#!/usr/bin/env python3
"""
Test script to generate a high-quality marketing poster
This tests the trained ML model for design generation
"""

import requests
import json
import time
from datetime import datetime

ML_SERVICE_URL = "http://localhost:8001"
BACKEND_URL = "http://localhost:8000"

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def test_ml_service():
    """Check if ML service and model are ready"""
    print_header("🔍 Checking ML Service Status")
    
    try:
        # Check health
        health = requests.get(f"{ML_SERVICE_URL}/health").json()
        print(f"✅ ML Service: {health['status']}")
        print(f"✅ Model Loaded: {health['model_loaded']}")
        print(f"   GPU Available: {health['gpu_available']}")
        
        # Check model info
        model_info = requests.get(f"{ML_SERVICE_URL}/model-info").json()
        print(f"\n📊 Model Details:")
        print(f"   Type: {model_info['model_type']}")
        print(f"   Base: {model_info['base_model']}")
        print(f"   Device: {model_info['device']}")
        print(f"   Status: {model_info['message']}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def generate_poster(prompt, platform="instagram", format="post", industry="technology"):
    """Generate a marketing poster"""
    print_header(f"🎨 Generating Poster")
    print(f"Prompt: {prompt}")
    print(f"Platform: {platform}")
    print(f"Format: {format}")
    print(f"Industry: {industry}")
    
    payload = {
        "prompt": prompt,
        "platform": platform,
        "format": format,
        "industry": industry,
        "tone": "professional"
    }
    
    print("\n⏳ Generating (this may take 10-20 seconds)...")
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{ML_SERVICE_URL}/generate",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            blueprint = data.get('blueprint', {})
            generation_info = blueprint.get('_generation_info', {})
            
            print(f"\n✅ Generation Successful! (took {elapsed:.1f}s)")
            print(f"\n📋 Design Details:")
            print(f"   Method Used: {generation_info.get('method', 'unknown').upper()}")
            print(f"   Model Loaded: {generation_info.get('model_loaded', False)}")
            print(f"   Headline: {blueprint.get('headline', 'N/A')}")
            print(f"   Background: {blueprint.get('background', blueprint.get('background_color', 'N/A'))}")
            
            # Check for elements
            elements = blueprint.get('elements', blueprint.get('objects', []))
            print(f"   Elements: {len(elements)} design elements")
            
            # Show element types
            if elements:
                element_types = [e.get('type', 'unknown') for e in elements]
                print(f"   Element Types: {', '.join(set(element_types))}")
            
            # Display metadata if available
            metadata = blueprint.get('metadata', {})
            if metadata:
                print(f"\n📐 Canvas:")
                print(f"   Size: {metadata.get('width', 'N/A')}x{metadata.get('height', 'N/A')}px")
                print(f"   Platform: {metadata.get('platform', 'N/A')}")
                print(f"   Format: {metadata.get('format', 'N/A')}")
            
            return data
        else:
            print(f"❌ Generation Failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def save_design_json(design_data, filename="generated_poster.json"):
    """Save the generated design to a JSON file"""
    if not design_data:
        return
    
    filepath = f"/home/vikas/Desktop/adgenesis/{filename}"
    with open(filepath, 'w') as f:
        json.dump(design_data, f, indent=2)
    
    print(f"\n💾 Design saved to: {filepath}")

def main():
    print("\n" + "🚀 "*20)
    print("   AdGenesis - Poster Generation Test")
    print("   Testing Trained ML Model")
    print("🚀 "*20 + "\n")
    
    # Test 1: Check services
    if not test_ml_service():
        print("\n❌ ML Service not ready. Please start it first.")
        return
    
    # Test 2: Generate a high-quality poster
    test_prompts = [
        {
            "prompt": "Create a bold promotional poster for CleanFuel Protein Bar - Premium plant-based protein with 20g protein per bar. Show energetic fitness vibe with modern design.",
            "platform": "instagram",
            "format": "post",
            "industry": "food"
        },
        {
            "prompt": "Design a sleek tech product launch poster for AI-powered smartphone with breakthrough camera technology. Use futuristic gradients and clean typography.",
            "platform": "facebook",
            "format": "post",
            "industry": "technology"
        },
        {
            "prompt": "Create an elegant summer fashion sale banner - 50% OFF Premium Collection. Use luxury aesthetic with gold accents and minimalist layout.",
            "platform": "instagram",
            "format": "story",
            "industry": "fashion"
        }
    ]
    
    print_header("🎯 Running Test Scenarios")
    
    for i, test in enumerate(test_prompts, 1):
        print(f"\n{'─'*60}")
        print(f"Test #{i} of {len(test_prompts)}")
        print(f"{'─'*60}")
        
        result = generate_poster(**test)
        
        if result and i == 1:  # Save first design
            save_design_json(result, f"test_poster_{i}.json")
        
        if i < len(test_prompts):
            print("\n⏸  Waiting 3 seconds before next test...")
            time.sleep(3)
    
    print_header("✅ Testing Complete!")
    print("You can now:")
    print("1. Open http://localhost:3000 in your browser")
    print("2. Go to Design Studio")
    print("3. Enter any prompt and click 'Generate Design'")
    print("4. Check the browser console to see which method was used")
    print("\nThe generated design JSON files are saved in the project root.")

if __name__ == "__main__":
    main()
