"""
Real AI Image Generation Service
Uses Hugging Face Inference API via the official huggingface_hub library
"""

import os
import io
import base64
import asyncio
from typing import Optional, Dict, Any, List
from PIL import Image
from pathlib import Path
import json
import hashlib
from datetime import datetime

# Import HuggingFace Hub Inference Client
try:
    from huggingface_hub import InferenceClient
    HF_CLIENT_AVAILABLE = True
except ImportError:
    HF_CLIENT_AVAILABLE = False
    print("⚠️ huggingface_hub not installed. Run: pip install huggingface_hub")

# Configuration
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY", "")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "")

# Available models - Tested and working with HF Inference API
AVAILABLE_MODELS = {
    "sdxl": {
        "name": "Stable Diffusion XL",
        "hf_model": "stabilityai/stable-diffusion-xl-base-1.0",
        "description": "High quality, detailed images (RECOMMENDED)",
        "best_for": ["product", "realistic", "detailed"]
    },
    "sdxl-turbo": {
        "name": "SDXL Turbo",
        "hf_model": "stabilityai/sdxl-turbo",
        "description": "Fast generation, good quality",
        "best_for": ["quick", "drafts", "iterations"]
    },
    "sd-1-5": {
        "name": "Stable Diffusion 1.5",
        "hf_model": "runwayml/stable-diffusion-v1-5",
        "description": "Classic stable diffusion",
        "best_for": ["general", "reliable", "fast"]
    },
    "flux-schnell": {
        "name": "FLUX.1-schnell",
        "hf_model": "black-forest-labs/FLUX.1-schnell",
        "description": "Latest fast model from Black Forest Labs",
        "best_for": ["fast", "quality", "modern"]
    }
}

# Style presets for ad generation
STYLE_PRESETS = {
    "modern": {
        "suffix": ", modern design, clean aesthetic, professional, minimalist, high quality",
        "negative": "blurry, low quality, amateur, cluttered, messy"
    },
    "vibrant": {
        "suffix": ", vibrant colors, eye-catching, bold design, energetic, dynamic",
        "negative": "dull, muted colors, boring, static"
    },
    "elegant": {
        "suffix": ", elegant design, sophisticated, luxury, premium quality, refined",
        "negative": "cheap, tacky, gaudy, low quality"
    },
    "playful": {
        "suffix": ", playful design, fun, colorful, friendly, approachable",
        "negative": "serious, corporate, boring, dull"
    },
    "corporate": {
        "suffix": ", corporate design, professional, business, trustworthy, clean",
        "negative": "unprofessional, casual, messy, cluttered"
    },
    "minimalist": {
        "suffix": ", minimalist design, simple, clean, lots of white space, elegant",
        "negative": "cluttered, busy, complex, overwhelming"
    }
}

# Platform-specific prompt enhancements
PLATFORM_ENHANCEMENTS = {
    "instagram": "Instagram-worthy, social media optimized, engaging, scroll-stopping",
    "facebook": "Facebook ad style, engaging, social media optimized",
    "linkedin": "professional, business-appropriate, LinkedIn style",
    "twitter": "Twitter-optimized, concise, impactful",
    "youtube": "YouTube thumbnail style, eye-catching, high contrast",
    "tiktok": "TikTok style, trendy, youth-oriented, dynamic",
    "pinterest": "Pinterest aesthetic, inspirational, visually appealing"
}


class ImageGenerator:
    """AI Image Generation Service"""
    
    def __init__(self):
        self.hf_api_key = HUGGINGFACE_API_KEY
        self.replicate_api_key = REPLICATE_API_KEY
        self.stability_api_key = STABILITY_API_KEY
        self.cache_dir = Path("generated_images")
        self.cache_dir.mkdir(exist_ok=True)
        
    def _get_cache_key(self, prompt: str, model: str, width: int, height: int) -> str:
        """Generate cache key for generated images"""
        content = f"{prompt}_{model}_{width}_{height}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _enhance_prompt(self, prompt: str, platform: str = None, style: str = "modern") -> tuple:
        """Enhance prompt with style and platform-specific additions"""
        enhanced = prompt
        negative = "blurry, low quality, distorted, ugly, bad anatomy, watermark, signature, text"
        
        # Add style enhancement
        if style in STYLE_PRESETS:
            enhanced += STYLE_PRESETS[style]["suffix"]
            negative = STYLE_PRESETS[style]["negative"] + ", " + negative
        
        # Add platform enhancement
        if platform and platform.lower() in PLATFORM_ENHANCEMENTS:
            enhanced += f", {PLATFORM_ENHANCEMENTS[platform.lower()]}"
        
        # Always add quality boosters
        enhanced += ", 8k resolution, highly detailed, professional photography"
        
        return enhanced, negative
    
    async def generate_with_huggingface(
        self,
        prompt: str,
        model: str = "sdxl",
        width: int = 1024,
        height: int = 1024,
        negative_prompt: str = "",
        num_inference_steps: int = 25,
        guidance_scale: float = 7.5,
    ) -> Optional[bytes]:
        """Generate image using HuggingFace Hub InferenceClient"""
        
        if not HF_CLIENT_AVAILABLE:
            raise ValueError("huggingface_hub library not installed. Run: pip install huggingface_hub")
        
        if not self.hf_api_key:
            raise ValueError("HUGGINGFACE_API_KEY not set. Please set it in environment variables.")
        
        model_info = AVAILABLE_MODELS.get(model, AVAILABLE_MODELS["sdxl"])
        model_id = model_info["hf_model"]
        
        print(f"   🔗 Using model: {model_id}")
        
        try:
            # Create the inference client
            client = InferenceClient(token=self.hf_api_key)
            
            # Generate image using text_to_image
            # Run sync call in thread pool since InferenceClient is sync
            loop = asyncio.get_event_loop()
            
            def _generate():
                return client.text_to_image(
                    prompt,
                    model=model_id,
                    negative_prompt=negative_prompt if negative_prompt else None,
                    width=min(width, 1024),
                    height=min(height, 1024),
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                )
            
            # Run in executor to avoid blocking
            image = await loop.run_in_executor(None, _generate)
            
            print(f"   ✅ Image generated: {image.size}")
            
            # Convert PIL Image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            return img_byte_arr.getvalue()
            
        except Exception as e:
            print(f"   ❌ HF generation error: {e}")
            raise RuntimeError(f"Image generation failed: {str(e)}")
    
    async def generate_with_stability(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 1024,
        negative_prompt: str = "",
        style_preset: str = "photographic"
    ) -> Optional[bytes]:
        """Generate image using Stability AI API"""
        
        if not self.stability_api_key:
            raise ValueError("STABILITY_API_KEY not set")
        
        headers = {
            "Authorization": f"Bearer {self.stability_api_key}",
            "Content-Type": "application/json",
            "Accept": "image/png"
        }
        
        payload = {
            "text_prompts": [
                {"text": prompt, "weight": 1},
                {"text": negative_prompt, "weight": -1}
            ],
            "width": width,
            "height": height,
            "style_preset": style_preset,
            "samples": 1,
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.content
            else:
                raise RuntimeError(f"Generation failed: {response.text}")
    
    async def generate_ad_image(
        self,
        prompt: str,
        platform: str = "instagram",
        format: str = "post",
        style: str = "modern",
        model: str = "sdxl",  # Use SDXL as default - most reliable
        width: int = None,
        height: int = None
    ) -> Dict[str, Any]:
        """
        Generate an ad image with enhanced prompts
        
        Returns:
            Dict with image_data (base64), metadata, and generation info
        """
        
        # Get dimensions from format if not provided
        FORMAT_SIZES = {
            "square": (1024, 1024),
            "post": (1024, 1024),
            "story": (768, 1024),  # Adjusted for model limits
            "landscape": (1024, 768),
            "portrait": (768, 1024),
            "cover": (1024, 576),
            "banner": (1024, 256),
        }
        
        if width is None or height is None:
            width, height = FORMAT_SIZES.get(format, (1024, 1024))
        
        # Ensure dimensions are valid (must be multiples of 8 for SD)
        width = (width // 8) * 8
        height = (height // 8) * 8
        
        # Cap at 1024 for HF models
        width = min(width, 1024)
        height = min(height, 1024)
        
        # Enhance the prompt
        enhanced_prompt, negative_prompt = self._enhance_prompt(prompt, platform, style)
        
        print(f"🎨 Generating image:")
        print(f"   Prompt: {enhanced_prompt[:100]}...")
        print(f"   Size: {width}x{height}")
        print(f"   Model: {model}")
        
        try:
            # Use Hugging Face if API key is set
            if self.hf_api_key:
                image_bytes = await self.generate_with_huggingface(
                    prompt=enhanced_prompt,
                    model=model,
                    width=width,
                    height=height,
                    negative_prompt=negative_prompt
                )
            elif self.stability_api_key:
                image_bytes = await self.generate_with_stability(
                    prompt=enhanced_prompt,
                    width=width,
                    height=height,
                    negative_prompt=negative_prompt
                )
            else:
                # Return a placeholder response indicating API key needed
                return {
                    "success": False,
                    "error": "No API key configured. Please set HUGGINGFACE_API_KEY or STABILITY_API_KEY",
                    "image_data": None,
                    "placeholder": True
                }
            
            # Convert to base64
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            
            # Save to cache
            cache_key = self._get_cache_key(prompt, model, width, height)
            cache_path = self.cache_dir / f"{cache_key}.png"
            with open(cache_path, "wb") as f:
                f.write(image_bytes)
            
            return {
                "success": True,
                "image_data": image_base64,
                "image_url": f"/generated/{cache_key}.png",
                "width": width,
                "height": height,
                "model": model,
                "prompt": prompt,
                "enhanced_prompt": enhanced_prompt,
                "metadata": {
                    "platform": platform,
                    "format": format,
                    "style": style,
                    "generated_at": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            print(f"❌ Generation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "image_data": None
            }
    
    def get_available_models(self) -> List[Dict]:
        """Get list of available models"""
        return [
            {"id": k, **v} for k, v in AVAILABLE_MODELS.items()
        ]
    
    def get_style_presets(self) -> Dict:
        """Get available style presets"""
        return STYLE_PRESETS


# Singleton instance
image_generator = ImageGenerator()


# Quick test function
async def test_generation():
    """Test the image generation"""
    result = await image_generator.generate_ad_image(
        prompt="A sleek smartphone floating in space with colorful nebula background",
        platform="instagram",
        format="post",
        style="modern"
    )
    print(json.dumps({k: v for k, v in result.items() if k != "image_data"}, indent=2))
    return result


if __name__ == "__main__":
    asyncio.run(test_generation())
