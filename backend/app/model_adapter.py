"""
Model adapter to switch between OpenAI and custom ML model
"""
import os
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

# Configuration
MODEL_PROVIDER: Literal["openai", "custom"] = os.getenv("MODEL_PROVIDER", "openai")
ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://localhost:8001")


class ModelAdapter:
    """Adapter to switch between different model providers"""
    
    def __init__(self, provider: str = MODEL_PROVIDER):
        """
        Initialize model adapter
        
        Args:
            provider: "openai" or "custom"
        """
        self.provider = provider
        
        if provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif provider == "custom":
            import sys
            from pathlib import Path
            # Add ml_pipeline to path
            ml_pipeline_path = Path(__file__).parent.parent.parent / "ml_pipeline"
            sys.path.insert(0, str(ml_pipeline_path))
            from client import MLModelClient
            self.client = MLModelClient(base_url=ML_SERVICE_URL)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    async def generate_design_spec(
        self,
        prompt: str,
        platform: str,
        format: str,
        specs: dict,
    ) -> dict:
        """
        Generate design specification
        
        Args:
            prompt: User's design prompt
            platform: Platform name
            format: Format name
            specs: Platform specifications
        
        Returns:
            Design specification dict
        """
        if self.provider == "openai":
            return await self._generate_with_openai(prompt, platform, format, specs)
        else:
            return await self._generate_with_custom_model(prompt, platform, format, specs)
    
    async def _generate_with_openai(
        self,
        prompt: str,
        platform: str,
        format: str,
        specs: dict,
    ) -> dict:
        """Generate using OpenAI API"""
        import json
        
        system_prompt = f"""You are an expert ad designer. Generate a detailed design specification for an advertisement.
Platform: {platform}
Format: {format} ({specs['width']}x{specs['height']})
User Request: {prompt}

Return a JSON structure with:
- background_color (hex)
- elements (list of text, shapes, images with positions, sizes, colors, fonts)
- layout (composition rules)

Make it professional, eye-catching, and platform-compliant."""

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    async def _generate_with_custom_model(
        self,
        prompt: str,
        platform: str,
        format: str,
        specs: dict,
    ) -> dict:
        """Generate using custom ML model"""
        result = await self.client.generate_design(
            prompt=prompt,
            platform=platform,
            format=format,
        )
        return result


# Global adapter instance
_adapter = None


def get_model_adapter() -> ModelAdapter:
    """Get or create the global model adapter"""
    global _adapter
    if _adapter is None:
        _adapter = ModelAdapter()
    return _adapter
