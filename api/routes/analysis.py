# ==============================================================================
# api/routes/analysis.py
# ==============================================================================
"""Analysis API routes"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from services.analysis_service import AnalysisService
from models.api_models import AnalysisRequest, AnalysisResponse, BatchAnalysisResponse
from utils.exceptions import AnalysisServiceError, ImageProcessingError
import logging
from typing import List
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/analysis", tags=["analysis"])

def get_analysis_service() -> AnalysisService:
    """Dependency to get analysis service"""
    return AnalysisService()

@router.post("/single", response_model=AnalysisResponse)
async def analyze_single_design(
    file: UploadFile = File(...),
    locations: str = "USA,India,UK",
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    """Analyze single t-shirt design"""
    
    try:
        # Parse locations
        location_list = [loc.strip() for loc in locations.split(",")]
        
        # Read image data
        image_data = await file.read()
        
        # Perform analysis
        result = await analysis_service.analyze_tshirt_design(
            image_data, location_list, file.filename or "upload.jpg"
        )
        
        return AnalysisResponse(
            success=True,
            data=result.to_dict()
        )
        
    except (ImageProcessingError, AnalysisServiceError) as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/batch", response_model=BatchAnalysisResponse)
async def analyze_batch_designs(
    files: List[UploadFile] = File(...),
    locations: str = "USA,India,UK",
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    """Analyze multiple t-shirt designs"""
    
    location_list = [loc.strip() for loc in locations.split(",")]
    results = []
    errors = []
    successful = 0
    
    for file in files:
        try:
            image_data = await file.read()
            result = await analysis_service.analyze_tshirt_design(
                image_data, location_list, file.filename or "upload.jpg"
            )
            
            results.append({
                "filename": file.filename,
                "analysis": result.to_dict()
            })
            successful += 1
            
        except Exception as e:
            error_msg = f"{file.filename}: {str(e)}"
            errors.append(error_msg)
            logger.error(error_msg)
    
    return BatchAnalysisResponse(
        total_processed=len(files),
        successful=successful,
        failed=len(files) - successful,
        results=results,
        errors=errors
    )
