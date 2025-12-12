"""
Test script to verify ML pipeline is working
"""
import asyncio
import json
from client import MLModelClient


async def test_ml_service():
    """Test the ML service"""
    print("🧪 Testing ML Service")
    print("=" * 50)
    
    async with MLModelClient(base_url="http://localhost:8001") as client:
        # Test 1: Health check
        print("\n1️⃣ Health Check")
        try:
            health = await client.health_check()
            print(f"✅ Service is healthy: {health}")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return
        
        # Test 2: List models
        print("\n2️⃣ List Models")
        try:
            models = await client.list_models()
            print(f"✅ Available models: {len(models)}")
            for model in models:
                print(f"   - {model['name']}")
        except Exception as e:
            print(f"⚠️  Could not list models: {e}")
        
        # Test 3: Generate design
        print("\n3️⃣ Generate Design")
        test_cases = [
            {
                "prompt": "Create a modern tech startup ad",
                "platform": "meta",
                "format": "square",
            },
            {
                "prompt": "Design a fashion sale ad",
                "platform": "meta",
                "format": "story",
            },
            {
                "prompt": "Create a B2B software ad",
                "platform": "linkedin",
                "format": "landscape",
            },
        ]
        
        for i, test in enumerate(test_cases, 1):
            print(f"\n   Test {i}: {test['prompt']}")
            try:
                design = await client.generate_design(**test)
                print(f"   ✅ Generated design:")
                print(f"      - Background: {design.get('background_color', 'N/A')}")
                print(f"      - Elements: {len(design.get('elements', []))}")
                
                # Show first element
                if design.get('elements'):
                    first_elem = design['elements'][0]
                    print(f"      - First element: {first_elem.get('type')} - {first_elem.get('text', 'N/A')[:50]}")
            except Exception as e:
                print(f"   ❌ Failed: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Testing complete!")


if __name__ == "__main__":
    print("Make sure the ML service is running:")
    print("  python serve.py --model gpt2")
    print("")
    
    try:
        asyncio.run(test_ml_service())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted")
