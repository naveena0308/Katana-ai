
# ==============================================================================
# PROJECT STRUCTURE
# ==============================================================================
"""
tshirt_analyzer/
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Project dependencies
├── .env                       # Environment variables
├── config/
│   ├── __init__.py
│   ├── settings.py            # Configuration settings
│   └── market_data.py         # Static market data
├── models/
│   ├── __init__.py
│   ├── data_models.py         # Pydantic/Dataclass models
│   └── api_models.py          # API request/response models
├── services/
│   ├── __init__.py
│   ├── gemini_service.py      # Gemini AI integration
│   ├── image_service.py       # Image processing utilities
│   ├── analysis_service.py    # Core analysis logic
│   └── market_service.py      # Market analysis logic
├── api/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── analysis.py        # Analysis endpoints
│   │   ├── market.py          # Market endpoints
│   │   └── trends.py          # Trends endpoints
│   └── dependencies.py        # FastAPI dependencies
├── utils/
│   ├── __init__.py
│   ├── validators.py          # Validation utilities
│   ├── helpers.py             # Helper functions
│   └── exceptions.py          # Custom exceptions
└── tests/
    ├── __init__.py
    ├── test_services.py
    ├── test_api.py
    └── fixtures/
"""

# ==============================================================================
# config/settings.py
# ==============================================================================
"""Configuration settings for the application"""
import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    app_name: str = "AI T-Shirt Market Analyzer"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Gemini AI Configuration
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = "gemini-1.5-flash"
    
    # File Upload Configuration
    max_file_size: int = 5 * 1024 * 1024  # 5MB
    supported_formats: List[str] = ["image/jpeg", "image/png", "image/webp"]
    max_image_dimension: int = 1024
    
    # Rate Limiting
    analysis_rate_limit: int = 100  # requests per hour
    
    # Database Configuration (for future use)
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./tshirt_analyzer.db")
    
    class Config:
        env_file = ".env"

settings = Settings()