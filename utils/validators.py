# ==============================================================================
# utils/validators.py
# ==============================================================================
"""Validation utilities"""
from typing import List
from config.market_data import MARKET_DATA
from utils.exceptions import ValidationError

def validate_locations(locations: List[str]) -> List[str]:
    """Validate and clean location list"""
    
    valid_locations = []
    invalid_locations = []
    
    for location in locations:
        location = location.strip().upper()
        if location in MARKET_DATA:
            valid_locations.append(location)
        else:
            invalid_locations.append(location)
    
    if invalid_locations:
        available = ", ".join(MARKET_DATA.keys())
        raise ValidationError(
            f"Invalid locations: {invalid_locations}. "
            f"Available: {available}"
        )
    
    if not valid_locations:
        raise ValidationError("At least one valid location is required")
    
    return valid_locations

def validate_file_type(content_type: str) -> bool:
    """Validate file content type"""
    from config.settings import settings
    return content_type in settings.supported_formats