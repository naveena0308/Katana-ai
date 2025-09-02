# ==============================================================================
# utils/exceptions.py
# ==============================================================================
"""Custom exception classes"""

class TShirtAnalyzerError(Exception):
    """Base exception for t-shirt analyzer"""
    pass

class ImageProcessingError(TShirtAnalyzerError):
    """Error in image processing"""
    pass

class AIServiceError(TShirtAnalyzerError):
    """Error in AI service calls"""
    pass

class AnalysisServiceError(TShirtAnalyzerError):
    """Error in analysis service"""
    pass

class ValidationError(TShirtAnalyzerError):
    """Validation error"""
    pass