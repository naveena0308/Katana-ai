# ==============================================================================
# services/analysis_service.py
# ==============================================================================
"""Core analysis orchestration service"""
import asyncio
import time
from typing import List, Dict, Any
from services.gemini_service import GeminiService
from services.image_service import ImageService
from services.market_service import MarketService
from models.data_models import AnalysisResult, DesignFeatures, MarketAnalysis
from config.market_data import MARKET_DATA
from utils.exceptions import AnalysisServiceError
import logging

logger = logging.getLogger(__name__)

class AnalysisService:
    """Main service for orchestrating t-shirt analysis"""
    
    def __init__(self):
        self.gemini_service = GeminiService()
        self.image_service = ImageService()
        self.market_service = MarketService()
    
    async def analyze_tshirt_design(self, image_data: bytes, locations: List[str],
                                  filename: str = "upload.jpg") -> AnalysisResult:
        """Complete t-shirt analysis pipeline"""
        start_time = time.time()
        
        try:
            # Step 1: Validate and process image
            self.image_service.validate_image(image_data, filename)
            processed_image, image_size = self.image_service.process_image(image_data)
            
            logger.info(f"Processing image: {filename}, size: {image_size}")
            
            # Step 2: AI design analysis
            design_features = await self.gemini_service.analyze_design_image(processed_image)
            logger.info(f"Design analysis complete: {design_features.style_category}")
            
            # Step 3: Market analysis for each location
            market_analyses = []
            analysis_tasks = []
            
            for location in locations:
                if location not in MARKET_DATA:
                    logger.warning(f"Unknown location: {location}")
                    continue
                
                task = self._analyze_single_market(design_features, location)
                analysis_tasks.append(task)
            
            # Run market analyses concurrently
            market_results = await asyncio.gather(*analysis_tasks, return_exceptions=True)
            
            for i, result in enumerate(market_results):
                if isinstance(result, Exception):
                    logger.error(f"Market analysis failed for {locations[i]}: {result}")
                    continue
                market_analyses.append(result)
            
            if not market_analyses:
                raise AnalysisServiceError("No successful market analyses")
            
            # Step 4: Generate overall score and recommendations
            overall_score = self._calculate_overall_score(market_analyses)
            recommendations = await self.gemini_service.generate_recommendations(
                design_features, [ma.to_dict() for ma in market_analyses]
            )
            
            # Step 5: Calculate confidence score
            confidence_score = self._calculate_confidence_score(design_features, market_analyses)
            
            processing_time = time.time() - start_time
            logger.info(f"Analysis complete in {processing_time:.2f}s")
            
            return AnalysisResult(
                design_features=design_features,
                market_analysis=market_analyses,
                overall_score=overall_score,
                recommendations=recommendations,
                analysis_timestamp=time.strftime('%Y-%m-%d %H:%M:%S'),
                confidence_score=confidence_score
            )
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            raise AnalysisServiceError(f"Analysis pipeline failed: {str(e)}")
    
    async def _analyze_single_market(self, design_features: DesignFeatures, 
                                   location: str) -> MarketAnalysis:
        """Analyze single market location"""
        
        market_context = MARKET_DATA[location]
        
        # Get AI market analysis
        ai_analysis = await self.gemini_service.generate_market_analysis(
            design_features, location, market_context
        )
        
        # Calculate pricing
        price_range = self.market_service.calculate_pricing(
            location, ai_analysis.get('market_score', 70)
        )
        
        return MarketAnalysis(
            location=location,
            market_score=float(ai_analysis.get('market_score', 70)),
            demand_level=ai_analysis.get('demand_level', 'medium'),
            price_range=price_range,
            competition_level=ai_analysis.get('competition_level', 'medium'),
            seasonal_trends=ai_analysis.get('seasonal_trends', ['year-round']),
            target_age_groups=ai_analysis.get('target_age_groups', ['18-35']),
            estimated_monthly_sales=int(ai_analysis.get('estimated_monthly_sales', 1000)),
            market_trends=ai_analysis.get('market_trends', []),
            success_probability=float(ai_analysis.get('success_probability', 70)),
            risk_factors=ai_analysis.get('risk_factors', []),
            opportunities=ai_analysis.get('opportunities', [])
        )
    
    def _calculate_overall_score(self, market_analyses: List[MarketAnalysis]) -> float:
        """Calculate weighted overall score"""
        if not market_analyses:
            return 0.0
        
        # Weight by market size and maturity
        total_weighted_score = 0.0
        total_weight = 0.0
        
        for analysis in market_analyses:
            market_info = MARKET_DATA.get(analysis.location, {})
            
            # Calculate weight based on market characteristics
            size_weight = {
                'massive': 1.5,
                'large': 1.2,
                'medium': 1.0,
                'small': 0.8
            }.get(market_info.get('market_size', 'medium'), 1.0)
            
            maturity_weight = {
                'mature': 1.1,
                'growing': 1.3,
                'emerging': 1.0
            }.get(market_info.get('market_maturity', 'mature'), 1.0)
            
            weight = size_weight * maturity_weight
            total_weighted_score += analysis.market_score * weight
            total_weight += weight
        
        return round(total_weighted_score / total_weight, 1) if total_weight > 0 else 0.0
    
    def _calculate_confidence_score(self, design_features: DesignFeatures,
                                  market_analyses: List[MarketAnalysis]) -> float:
        """Calculate analysis confidence score"""
        
        # Factors affecting confidence
        design_clarity = min(100, design_features.visual_appeal_score + design_features.uniqueness_score) / 2
        market_consistency = self._calculate_market_consistency(market_analyses)
        data_completeness = len(market_analyses) / 8 * 100  # Against max 8 locations
        
        confidence = (design_clarity * 0.4 + market_consistency * 0.4 + data_completeness * 0.2)
        return round(min(95, confidence), 1)
    
    def _calculate_market_consistency(self, market_analyses: List[MarketAnalysis]) -> float:
        """Calculate consistency across market analyses"""
        if len(market_analyses) < 2:
            return 80.0
        
        scores = [analysis.market_score for analysis in market_analyses]
        mean_score = sum(scores) / len(scores)
        variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
        std_dev = variance ** 0.5
        
        # Higher consistency = higher confidence
        consistency = max(0, 100 - (std_dev * 2))
        return round(consistency, 1)