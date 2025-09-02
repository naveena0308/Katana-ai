# ==============================================================================
# tests/test_services.py
# ==============================================================================
"""
Unit tests for services
"""
import pytest
import asyncio
from services.analysis_service import AnalysisService
from services.image_service import ImageService
from models.data_models import DesignFeatures

class TestAnalysisService:
    
    @pytest.fixture
    def analysis_service(self):
        return AnalysisService()
    
    @pytest.fixture
    def sample_image_data(self):
        # Create a simple test image
        from PIL import Image
        import io
        
        img = Image.new('RGB', (300, 300), color='red')
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        return buffer.getvalue()
    
    @pytest.mark.asyncio
    async def test_analyze_tshirt_design(self, analysis_service, sample_image_data):
        """Test complete analysis pipeline"""
        
        locations = ["USA", "India"]
        result = await analysis_service.analyze_tshirt_design(
            sample_image_data, locations, "test.jpg"
        )
        
        assert result.overall_score > 0
        assert len(result.market_analysis) == 2
        assert result.design_features.style_category is not None

class TestImageService:
    
    def test_validate_image(self):
        """Test image validation"""
        # Test with valid image data
        # Implementation depends on your test image setup
        pass