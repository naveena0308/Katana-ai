# ==============================================================================
# utils/helpers.py
# ==============================================================================
"""Helper utility functions"""
import hashlib
import time
from typing import Any, Dict
import json
from typing import List


def generate_analysis_id(image_data: bytes, locations: List[str]) -> str:
    """Generate unique ID for analysis"""
    
    content = f"{hashlib.md5(image_data).hexdigest()}_{sorted(locations)}_{int(time.time())}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]

def format_currency(amount: float, currency: str) -> str:
    """Format currency amount"""
    
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "INR": "₹",
        "BRL": "R$",
        "AUD": "A$",
        "CAD": "C$"
    }
    
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:.2f}"

def serialize_analysis(analysis_result) -> Dict[str, Any]:
    """Serialize analysis result for JSON response"""
    
    if hasattr(analysis_result, 'to_dict'):
        return analysis_result.to_dict()
    elif hasattr(analysis_result, '__dict__'):
        return analysis_result.__dict__
    else:
        return analysis_result