# ==============================================================================
# models/api_models.py
# ==============================================================================
"""API request/response models"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class AnalysisRequest(BaseModel):
    locations: List[str] = Field(..., description="List of locations to analyze")
    include_trends: bool = Field(default=False, description="Include trend analysis")
    include_competition: bool = Field(default=False, description="Include competition analysis")

class AnalysisResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    processing_time: Optional[float] = None

class LocationInfo(BaseModel):
    code: str
    name: str
    description: str
    currency: str
    market_size: str

class TrendAnalysisRequest(BaseModel):
    timeframe: str = Field(default="current", description="Timeframe for trend analysis")
    categories: List[str] = Field(default=[], description="Specific categories to analyze")

class CompetitorAnalysisRequest(BaseModel):
    design_description: str
    target_market: str
    price_range: Optional[Dict[str, float]] = None

class BatchAnalysisResponse(BaseModel):
    total_processed: int
    successful: int
    failed: int
    results: List[Dict[str, Any]]
    errors: List[str]