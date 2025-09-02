# ==============================================================================
# api/routes/trends.py
# ==============================================================================
"""Trends analysis API routes"""
from fastapi import APIRouter, HTTPException, Depends
from services.gemini_service import GeminiService
from models.api_models import TrendAnalysisRequest, CompetitorAnalysisRequest
from utils.exceptions import AIServiceError
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/trends", tags=["trends"])

@router.post("/current")
async def analyze_current_trends(request: TrendAnalysisRequest = None):
    """Analyze current market trends"""
    
    if request is None:
        request = TrendAnalysisRequest()
    
    try:
        gemini_service = GeminiService()
        trends = await gemini_service.analyze_trends(request.timeframe)
        
        return {
            "timeframe": request.timeframe,
            "trends": trends,
            "analysis_date": "2025-09-01"
        }
        
    except AIServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/competitor-analysis")
async def analyze_competitors(request: CompetitorAnalysisRequest):
    """Analyze competitive landscape"""
    
    try:
        gemini_service = GeminiService()
        
        prompt = f"""
        Analyze competitive landscape for t-shirt design in {request.target_market}.
        
        Design Description: {request.design_description}
        Price Range: {request.price_range or 'Not specified'}
        
        Provide analysis on:
        1. Major competitors and market leaders
        2. Similar designs currently in market
        3. Price positioning strategies
        4. Market gaps and opportunities
        5. Differentiation strategies needed
        6. Competitive advantages to develop
        7. Market entry barriers
        
        Return structured JSON analysis.
        """
        
        response = await gemini_service.model.generate_content(prompt)
        analysis = gemini_service._parse_json_response(response.text)
        
        return {
            "target_market": request.target_market,
            "competitive_analysis": analysis
        }
        
    except Exception as e:
        logger.error(f"Competitor analysis error: {e}")
        raise HTTPException(status_code=500, detail="Competitor analysis failed")