# ==============================================================================
# models/data_models.py
# ==============================================================================
"""Data models and schemas"""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

class DemandLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class CompetitionLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class BrandPotential(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class DesignFeatures:
    """Design analysis results from AI"""
    style_category: str
    color_palette: List[str]
    design_complexity: str
    target_demographic: str
    theme_category: str
    visual_appeal_score: float
    uniqueness_score: float
    brand_potential: str
    typography_quality: Optional[float] = None
    graphic_elements: Optional[List[str]] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class MarketAnalysis:
    """Market analysis results for a specific location"""
    location: str
    market_score: float
    demand_level: DemandLevel
    price_range: Dict[str, float]
    competition_level: CompetitionLevel
    seasonal_trends: List[str]
    target_age_groups: List[str]
    estimated_monthly_sales: int
    market_trends: List[str]
    success_probability: float
    risk_factors: Optional[List[str]] = None
    opportunities: Optional[List[str]] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class AnalysisResult:
    """Complete analysis result"""
    design_features: DesignFeatures
    market_analysis: List[MarketAnalysis]
    overall_score: float
    recommendations: List[str]
    analysis_timestamp: str
    confidence_score: Optional[float] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class TrendAnalysis:
    """Market trend analysis"""
    trend_name: str
    relevance_score: float
    growth_rate: str
    target_demographics: List[str]
    geographic_relevance: List[str]
    seasonal_pattern: Optional[str] = None