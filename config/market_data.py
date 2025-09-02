# ==============================================================================
# config/market_data.py
# ==============================================================================
"""Static market data and configurations"""
from typing import Dict, List

MARKET_DATA = {
    "USA": {
        "base_price_range": (15, 35),
        "market_size": "large",
        "currency": "USD",
        "trends": ["sustainability", "minimalism", "vintage", "streetwear"],
        "demographics": ["gen_z", "millennials", "gen_x"],
        "seasonal_peaks": ["summer", "back_to_school", "holidays"],
        "competition_level": "high",
        "market_maturity": "mature"
    },
    "India": {
        "base_price_range": (5, 15),
        "market_size": "massive",
        "currency": "INR",
        "trends": ["bollywood", "cricket", "festivals", "regional_pride"],
        "demographics": ["youth", "millennials"],
        "seasonal_peaks": ["festivals", "cricket_season", "summer"],
        "competition_level": "high",
        "market_maturity": "growing"
    },
    "UK": {
        "base_price_range": (12, 28),
        "market_size": "medium",
        "currency": "GBP",
        "trends": ["british_humor", "football", "music", "royal_themes"],
        "demographics": ["millennials", "gen_x"],
        "seasonal_peaks": ["summer", "football_season"],
        "competition_level": "medium",
        "market_maturity": "mature"
    },
    "Germany": {
        "base_price_range": (18, 40),
        "market_size": "medium",
        "currency": "EUR",
        "trends": ["quality", "minimalism", "eco_friendly", "engineering"],
        "demographics": ["millennials", "gen_x"],
        "seasonal_peaks": ["summer", "oktoberfest"],
        "competition_level": "medium",
        "market_maturity": "mature"
    },
    "Japan": {
        "base_price_range": (20, 45),
        "market_size": "medium",
        "currency": "JPY",
        "trends": ["anime", "kawaii", "tech", "minimalism"],
        "demographics": ["youth", "otaku", "salarymen"],
        "seasonal_peaks": ["summer", "manga_releases", "tech_events"],
        "competition_level": "high",
        "market_maturity": "mature"
    },
    "Brazil": {
        "base_price_range": (8, 20),
        "market_size": "large",
        "currency": "BRL",
        "trends": ["football", "carnival", "beach", "music"],
        "demographics": ["youth", "sports_fans"],
        "seasonal_peaks": ["summer", "world_cup", "carnival"],
        "competition_level": "medium",
        "market_maturity": "growing"
    },
    "Australia": {
        "base_price_range": (16, 38),
        "market_size": "medium",
        "currency": "AUD",
        "trends": ["surf", "outdoor", "casual", "sports"],
        "demographics": ["millennials", "outdoor_enthusiasts"],
        "seasonal_peaks": ["summer", "sports_season"],
        "competition_level": "medium",
        "market_maturity": "mature"
    },
    "Canada": {
        "base_price_range": (14, 32),
        "market_size": "medium",
        "currency": "CAD",
        "trends": ["hockey", "nature", "maple", "winter_sports"],
        "demographics": ["millennials", "gen_x"],
        "seasonal_peaks": ["summer", "hockey_season", "winter_olympics"],
        "competition_level": "medium",
        "market_maturity": "mature"
    }
}

DESIGN_CATEGORIES = {
    "style": ["minimalist", "vintage", "modern", "artistic", "streetwear", "corporate", "casual", "luxury"],
    "complexity": ["simple", "moderate", "complex"],
    "demographics": ["gen_z", "millennials", "gen_x", "baby_boomers", "all_ages"],
    "themes": ["abstract", "pop_culture", "motivational", "sports", "music", "art", "technology", "nature"],
    "brand_potential": ["low", "medium", "high"]
}
