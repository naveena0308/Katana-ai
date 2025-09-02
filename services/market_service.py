# ==============================================================================
# services/market_service.py
# ==============================================================================
"""Market analysis and pricing service"""
from typing import Dict, List, Any
from config.market_data import MARKET_DATA
from models.data_models import DesignFeatures
import logging

logger = logging.getLogger(__name__)

class MarketService:
    """Service for market analysis and pricing calculations"""
    
    def __init__(self):
        self.market_data = MARKET_DATA
    
    def calculate_pricing(self, location: str, market_score: float) -> Dict[str, float]:
        """Calculate optimal pricing for location based on market score"""
        
        market_info = self.market_data.get(location, self.market_data["USA"])
        base_min, base_max = market_info["base_price_range"]
        
        # Adjust pricing based on market score and local factors
        score_multiplier = market_score / 75.0  # Base score of 75
        
        # Apply market-specific adjustments
        market_adjustments = {
            "Germany": 1.1,  # Premium market
            "Japan": 1.15,   # High-value market
            "India": 0.9,    # Price-sensitive
            "Brazil": 0.95,  # Emerging market
        }
        
        adjustment = market_adjustments.get(location, 1.0)
        
        final_min = round(base_min * score_multiplier * adjustment, 2)
        final_max = round(base_max * score_multiplier * adjustment, 2)
        
        return {
            "min": final_min,
            "max": final_max,
            "recommended": round((final_min + final_max) / 2, 2),
            "currency": market_info.get("currency", "USD")
        }
    
    def get_market_insights(self, location: str) -> Dict[str, Any]:
        """Get detailed market insights for location"""
        
        if location not in self.market_data:
            raise ValueError(f"Location {location} not supported")
        
        market_info = self.market_data[location]
        
        return {
            "location": location,
            "market_size": market_info["market_size"],
            "competition_level": market_info["competition_level"],
            "market_maturity": market_info["market_maturity"],
            "key_trends": market_info["trends"],
            "target_demographics": market_info["demographics"],
            "seasonal_peaks": market_info["seasonal_peaks"],
            "base_price_range": market_info["base_price_range"],
            "currency": market_info["currency"]
        }
    
    def calculate_market_opportunity(self, design_features: DesignFeatures,
                                   location: str) -> Dict[str, Any]:
        """Calculate market opportunity score"""
        
        market_info = self.market_data[location]
        
        # Calculate trend alignment
        trend_alignment = self._calculate_trend_alignment(
            design_features, market_info["trends"]
        )
        
        # Calculate demographic fit
        demographic_fit = self._calculate_demographic_fit(
            design_features, market_info["demographics"]
        )
        
        # Market size factor
        size_factor = {
            "massive": 1.3,
            "large": 1.1,
            "medium": 1.0,
            "small": 0.8
        }.get(market_info["market_size"], 1.0)
        
        opportunity_score = (trend_alignment * 0.4 + demographic_fit * 0.4) * size_factor * 100
        
        return {
            "opportunity_score": round(min(100, opportunity_score), 1),
            "trend_alignment": round(trend_alignment * 100, 1),
            "demographic_fit": round(demographic_fit * 100, 1),
            "market_size_factor": size_factor
        }
    
    def _calculate_trend_alignment(self, design_features: DesignFeatures,
                                 local_trends: List[str]) -> float:
        """Calculate how well design aligns with local trends"""
        
        # Map design features to trend categories
        feature_trends = {
            "minimalist": ["minimalism", "quality", "simplicity"],
            "vintage": ["vintage", "retro", "nostalgia"],
            "streetwear": ["urban", "youth", "hip_hop"],
            "sports": ["sports", "fitness", "athletic"],
            "artistic": ["art", "creativity", "expression"]
        }
        
        design_trend_words = feature_trends.get(design_features.style_category, [])
        design_trend_words.extend([design_features.theme_category])
        
        # Calculate overlap
        matches = sum(1 for trend in local_trends 
                     if any(word in trend for word in design_trend_words))
        
        return min(1.0, matches / len(local_trends) * 2)  # Boost alignment score
    
    def _calculate_demographic_fit(self, design_features: DesignFeatures,
                                 target_demographics: List[str]) -> float:
        """Calculate demographic alignment"""
        
        demo_map = {
            "gen_z": ["youth", "gen_z", "teens"],
            "millennials": ["millennials", "young_adults"],
            "gen_x": ["gen_x", "adults"],
            "all_ages": ["all_ages", "universal"]
        }
        
        design_demo_words = demo_map.get(design_features.target_demographic, [])
        
        matches = sum(1 for demo in target_demographics
                     if any(word in demo for word in design_demo_words))
        
        return min(1.0, matches / len(target_demographics) * 1.5)
