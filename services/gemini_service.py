# ==============================================================================
# services/gemini_service.py
# ==============================================================================
"""Google Gemini AI integration service"""
import json
import base64
import asyncio
from typing import Dict, Any, Optional
import google.generativeai as genai
from config.settings import settings
from models.data_models import DesignFeatures
from typing import List
from utils.exceptions import AIServiceError
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    """Service for interacting with Google Gemini AI"""
    
    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)
    
    async def analyze_design_image(self, image_data: bytes) -> DesignFeatures:
        """Analyze t-shirt design using Gemini Vision"""
        
        try:
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            prompt = self._get_design_analysis_prompt()
            
            image_part = {
                "mime_type": "image/jpeg",
                "data": image_base64
            }
            
            response = await asyncio.to_thread(
                self.model.generate_content, 
                [prompt, image_part]
            )
            
            analysis_data = self._parse_json_response(response.text)
            
            return DesignFeatures(
                style_category=analysis_data.get("style_category", "modern"),
                color_palette=analysis_data.get("color_palette", ["unknown"]),
                design_complexity=analysis_data.get("design_complexity", "moderate"),
                target_demographic=analysis_data.get("target_demographic", "millennials"),
                theme_category=analysis_data.get("theme_category", "abstract"),
                visual_appeal_score=float(analysis_data.get("visual_appeal_score", 75)),
                uniqueness_score=float(analysis_data.get("uniqueness_score", 70)),
                brand_potential=analysis_data.get("brand_potential", "medium"),
                typography_quality=analysis_data.get("typography_quality"),
                graphic_elements=analysis_data.get("graphic_elements", [])
            )
            
        except Exception as e:
            logger.error(f"Error in Gemini design analysis: {e}")
            raise AIServiceError(f"Design analysis failed: {str(e)}")
    
    async def generate_market_analysis(self, design_features: DesignFeatures, 
                                     location: str, market_context: Dict) -> Dict[str, Any]:
        """Generate market analysis using Gemini"""
        
        try:
            prompt = self._get_market_analysis_prompt(design_features, location, market_context)
            
            response = await asyncio.to_thread(
                self.model.generate_content, 
                prompt
            )
            
            return self._parse_json_response(response.text)
            
        except Exception as e:
            logger.error(f"Error in Gemini market analysis for {location}: {e}")
            raise AIServiceError(f"Market analysis failed for {location}: {str(e)}")
    
    async def generate_recommendations(self, design_features: DesignFeatures,
                                     market_analyses: List[Dict]) -> List[str]:
        """Generate strategic recommendations"""
        
        try:
            prompt = self._get_recommendations_prompt(design_features, market_analyses)
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            
            recommendations_data = self._parse_json_response(response.text)
            return recommendations_data.get("recommendations", [])
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return [
                "Focus on highest scoring markets first",
                "Implement dynamic pricing strategy",
                "Target social media marketing"
            ]
    
    async def analyze_trends(self, timeframe: str = "current") -> Dict[str, Any]:
        """Analyze current market trends"""
        
        try:
            prompt = f"""
            Analyze current t-shirt market trends for {timeframe} period.
            
            Provide insights on:
            1. Popular design styles and their growth rates
            2. Color trends and seasonal patterns
            3. Emerging themes and cultural influences
            4. Consumer behavior changes post-pandemic
            5. Technology impact (AI, personalization, sustainability)
            6. Regional preference differences
            7. Price sensitivity changes
            
            Return as structured JSON with specific metrics where possible.
            """
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            
            return self._parse_json_response(response.text)
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            raise AIServiceError(f"Trend analysis failed: {str(e)}")
    
    def _get_design_analysis_prompt(self) -> str:
        """Get design analysis prompt"""
        return """
        Analyze this t-shirt design image comprehensively. Evaluate:
        
        1. **style_category**: minimalist, vintage, modern, artistic, streetwear, corporate, casual, luxury
        2. **color_palette**: List main colors used (e.g., ["blue", "white", "red"])
        3. **design_complexity**: simple, moderate, complex
        4. **target_demographic**: gen_z, millennials, gen_x, baby_boomers, all_ages
        5. **theme_category**: abstract, pop_culture, motivational, sports, music, art, technology, nature
        6. **visual_appeal_score**: 0-100 based on current design trends and aesthetic quality
        7. **uniqueness_score**: 0-100 based on how distinctive/original the design is
        8. **brand_potential**: low, medium, high - scalability as a brand
        9. **typography_quality**: 0-100 if text is present, null if no text
        10. **graphic_elements**: List of graphic elements present
        
        Consider current fashion trends, color psychology, target audience preferences, 
        and commercial viability. Be specific and analytical.
        
        Return ONLY valid JSON with these exact field names.
        """
    
    def _get_market_analysis_prompt(self, design_features: DesignFeatures, 
                                  location: str, market_context: Dict) -> str:
        """Get market analysis prompt"""
        return f"""
        Analyze market potential for this t-shirt design in {location}.
        
        Design Profile:
        - Style: {design_features.style_category}
        - Colors: {', '.join(design_features.color_palette)}
        - Complexity: {design_features.design_complexity}
        - Target Demo: {design_features.target_demographic}
        - Theme: {design_features.theme_category}
        - Visual Appeal: {design_features.visual_appeal_score}/100
        - Uniqueness: {design_features.uniqueness_score}/100
        
        {location} Market Context:
        - Trends: {', '.join(market_context.get('trends', []))}
        - Demographics: {', '.join(market_context.get('demographics', []))}
        - Market Size: {market_context.get('market_size')}
        - Competition: {market_context.get('competition_level')}
        
        Provide detailed analysis:
        
        {{
            "market_score": 0-100,
            "demand_level": "low/medium/high",
            "competition_level": "low/medium/high",
            "seasonal_trends": ["season1", "season2"],
            "target_age_groups": ["18-25", "26-35"],
            "market_trends": ["trend1", "trend2", "trend3"],
            "success_probability": 0-100,
            "estimated_monthly_sales": realistic_number,
            "risk_factors": ["risk1", "risk2"],
            "opportunities": ["opp1", "opp2"]
        }}
        
        Consider local culture, economic factors, fashion preferences, and seasonal patterns.
        Be realistic and data-driven in your analysis.
        """
    
    def _get_recommendations_prompt(self, design_features: DesignFeatures,
                                  market_analyses: List[Dict]) -> str:
        """Get recommendations prompt"""
        market_summary = {
            analysis['location']: {
                'score': analysis['market_score'],
                'demand': analysis['demand_level'],
                'sales': analysis['estimated_monthly_sales']
            }
            for analysis in market_analyses
        }
        
        return f"""
        Generate strategic business recommendations based on this analysis:
        
        Design Strengths:
        - Visual Appeal: {design_features.visual_appeal_score}/100
        - Uniqueness: {design_features.uniqueness_score}/100
        - Brand Potential: {design_features.brand_potential}
        
        Market Performance Summary:
        {json.dumps(market_summary, indent=2)}
        
        Provide 5-7 specific, actionable recommendations covering:
        1. Market entry strategy and prioritization
        2. Pricing optimization across regions
        3. Marketing and promotion tactics
        4. Production and inventory planning
        5. Risk mitigation strategies
        6. Growth opportunities
        
        Return as JSON: {{"recommendations": ["rec1", "rec2", ...]}}
        
        Make recommendations specific, measurable, and implementable.
        """
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON from Gemini response"""
        try:
            # Clean response text
            text = response_text.strip()
            
            # Extract JSON from markdown blocks
            if "```json" in text:
                start = text.find("```json") + 7
                end = text.find("```", start)
                text = text[start:end].strip()
            elif "```" in text:
                start = text.find("```") + 3
                end = text.find("```", start)
                text = text[start:end].strip()
            
            return json.loads(text)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response text: {response_text}")
            raise AIServiceError("Invalid JSON response from AI service")