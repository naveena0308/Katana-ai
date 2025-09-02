# ==============================================================================
# main.py
# ==============================================================================
"""FastAPI application entry point"""
import logging
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config.settings import settings
from api.routes import analysis, market, trends
from utils.exceptions import TShirtAnalyzerError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("🚀 Starting AI T-Shirt Market Analyzer")
    logger.info(f"📊 Powered by Google Gemini AI ({settings.gemini_model})")
    yield
    logger.info("🛑 Shutting down AI T-Shirt Market Analyzer")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered t-shirt market analysis using Google Gemini",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Global exception handler
@app.exception_handler(TShirtAnalyzerError)
async def analyzer_exception_handler(request: Request, exc: TShirtAnalyzerError):
    return JSONResponse(
        status_code=400,
        content={"success": False, "error": str(exc)}
    )

# Include routers
app.include_router(analysis.router)
app.include_router(market.router)
app.include_router(trends.router)

@app.get("/")
async def root():
    """API status endpoint"""
    return {
        "message": f"{settings.app_name} API",
        "version": settings.app_version,
        "status": "active",
        "endpoints": {
            "analysis": "/api/v1/analysis/single",
            "batch": "/api/v1/analysis/batch",
            "markets": "/api/v1/market/locations",
            "trends": "/api/v1/trends/current"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "gemini_configured": bool(settings.gemini_api_key)
    }

# if __name__ == "__main__":
#     import uvicorn
    
#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=settings.debug,
#         log_level="info"
#     )