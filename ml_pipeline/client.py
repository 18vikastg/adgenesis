"""
Python client for ML model service
"""
import httpx
from typing import Optional
import json


class MLModelClient:
    """Client for interacting with the ML model inference service"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        """
        Initialize client
        
        Args:
            base_url: Base URL of the ML service
        """
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(timeout=120.0)
    
    async def health_check(self) -> dict:
        """Check if the service is healthy"""
        response = await self.client.get(f"{self.base_url}/")
        response.raise_for_status()
        return response.json()
    
    async def generate_design(
        self,
        prompt: str,
        platform: str,
        format: str,
    ) -> dict:
        """
        Generate ad design specification
        
        Args:
            prompt: User's design prompt
            platform: Platform name (meta, google, linkedin)
            format: Format (square, landscape, portrait, story)
        
        Returns:
            Design specification dict with background_color, elements, layout
        """
        payload = {
            "prompt": prompt,
            "platform": platform,
            "format": format,
        }
        
        response = await self.client.post(
            f"{self.base_url}/generate",
            json=payload,
        )
        response.raise_for_status()
        return response.json()
    
    async def list_models(self) -> list:
        """List available models"""
        response = await self.client.get(f"{self.base_url}/models")
        response.raise_for_status()
        return response.json()["models"]
    
    async def close(self):
        """Close the client connection"""
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# Example usage
async def example_usage():
    """Example of how to use the client"""
    async with MLModelClient() as client:
        # Health check
        health = await client.health_check()
        print(f"Service status: {health}")
        
        # Generate design
        design = await client.generate_design(
            prompt="Create a modern tech startup ad",
            platform="meta",
            format="square",
        )
        print(f"Generated design: {json.dumps(design, indent=2)}")
        
        # List models
        models = await client.list_models()
        print(f"Available models: {models}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())
