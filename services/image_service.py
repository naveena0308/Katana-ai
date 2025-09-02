# ==============================================================================
# services/image_service.py
# ==============================================================================
"""Image processing and validation service"""
from PIL import Image
import io
from typing import Tuple, Optional
from config.settings import settings
from utils.exceptions import ImageProcessingError
import logging

logger = logging.getLogger(__name__)

class ImageService:
    """Service for image processing and validation"""
    
    @staticmethod
    def validate_image(image_data: bytes, filename: str) -> bool:
        """Validate uploaded image"""
        try:
            # Check file size
            if len(image_data) > settings.max_file_size:
                raise ImageProcessingError("File size exceeds maximum limit")
            
            # Check if it's a valid image
            image = Image.open(io.BytesIO(image_data))
            
            # Check format
            if image.format.lower() not in ['jpeg', 'jpg', 'png', 'webp']:
                raise ImageProcessingError("Unsupported image format")
            
            # Check dimensions (reasonable limits)
            if max(image.size) < 100:
                raise ImageProcessingError("Image too small (minimum 100px)")
            
            if max(image.size) > 4000:
                logger.warning(f"Large image detected: {image.size}")
            
            return True
            
        except Exception as e:
            if isinstance(e, ImageProcessingError):
                raise
            raise ImageProcessingError(f"Invalid image file: {str(e)}")
    
    @staticmethod
    def process_image(image_data: bytes) -> Tuple[bytes, Tuple[int, int]]:
        """Process and optimize image for AI analysis"""
        try:
            image = Image.open(io.BytesIO(image_data))
            original_size = image.size
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize if too large
            max_dim = settings.max_image_dimension
            if max(image.size) > max_dim:
                ratio = max_dim / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)
                logger.info(f"Resized image from {original_size} to {new_size}")
            
            # Optimize and compress
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', quality=85, optimize=True)
            processed_data = buffer.getvalue()
            
            return processed_data, image.size
            
        except Exception as e:
            raise ImageProcessingError(f"Image processing failed: {str(e)}")
    
    @staticmethod
    def extract_image_metadata(image_data: bytes) -> dict:
        """Extract metadata from image"""
        try:
            image = Image.open(io.BytesIO(image_data))
            
            metadata = {
                "format": image.format,
                "mode": image.mode,
                "size": image.size,
                "has_transparency": image.mode in ('RGBA', 'LA') or 'transparency' in image.info
            }
            
            # Extract EXIF data if available
            if hasattr(image, '_getexif'):
                exif = image._getexif()
                if exif:
                    metadata["exif"] = dict(exif)
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error extracting image metadata: {e}")
            return {}