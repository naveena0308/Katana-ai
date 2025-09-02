# ==============================================================================
# api/routes/market.py
# ==============================================================================
"""Market-related API routes"""
from fastapi import APIRouter, HTTPException, Depends
from services.market_service import MarketService
from services.gemini_service import GeminiService
from models.api_models import LocationInfo
from config.market_data import MARKET_DATA
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/market", tags=["market"])

@router.get("/locations")
async def get_locations():
    """Get all available analysis locations"""
    
    locations = []
    for code, data in MARKET_DATA.items():
        locations.append(LocationInfo(
            code=code,
            name=code,
            description=f"{data['market_size'].title()} {data['market_maturity']} market",
            currency=data.get('currency', 'USD'),
            market_size=data['market_size']
        ))
    
    return {"locations": locations}

@router.get("/insights/{location}")
async def get_market_insights(location: str):
    """Get detailed insights for specific market"""
    
    market_service = MarketService()
    
    try:
        insights = market_service.get_market_insights(location)
        
        # Get AI-generated insights
        gemini_service = GeminiService()
        ai_insights = await gemini_service.analyze_trends(timeframe="current")
        
        return {
            "market_data": insights,
            "ai_insights": ai_insights
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting market insights: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/compare/{location1}/{location2}")
async def compare_markets(location1: str, location2: str):
    """Compare two markets side by side"""
    
    market_service = MarketService()
    
    try:
        insights1 = market_service.get_market_insights(location1)
        insights2 = market_service.get_market_insights(location2)
        
        comparison = {
            "location1": insights1,
            "location2": insights2,
            "comparison_metrics": {
                "price_difference": {
                    "min": insights2["base_price_range"][0] - insights1["base_price_range"][0],
                    "max": insights2["base_price_range"][1] - insights1["base_price_range"][1]
                },
                "market_size_comparison": f"{insights1['market_size']} vs {insights2['market_size']}",
                "competition_comparison": f"{insights1['competition_level']} vs {insights2['competition_level']}"
            }
        }
        
        return comparison
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))