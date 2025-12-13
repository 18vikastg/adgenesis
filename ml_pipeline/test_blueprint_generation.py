#!/usr/bin/env python3
"""
Test script for design blueprint generation
Tests the complete pipeline: prompt -> ML service -> JSON blueprint
"""

import requests
import json
import sys

ML_SERVICE_URL = "http://localhost:8001"

def test_health():
    """Test ML service health"""
    print("🔍 Testing ML service health...")
    try:
        response = requests.get(f"{ML_SERVICE_URL}/health", timeout=5)
        print(f"✅ ML Service is healthy: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ ML Service health check failed: {e}")
        return False

def test_generation(prompt, platform="meta", format="square"):
    """Test design blueprint generation"""
    print(f"\n🎨 Testing design generation...")
    print(f"   Prompt: {prompt}")
    print(f"   Platform: {platform}")
    print(f"   Format: {format}")
    
    try:
        response = requests.post(
            f"{ML_SERVICE_URL}/generate",
            json={
                "prompt": prompt,
                "platform": platform,
                "format": format
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                blueprint = result["blueprint"]
                print(f"\n✅ Generation successful!")
                print(f"   Headline: {blueprint.get('headline')}")
                print(f"   Subheadline: {blueprint.get('subheadline')}")
                print(f"   CTA: {blueprint.get('cta_text')}")
                print(f"   Background: {blueprint.get('background', {}).get('color')}")
                print(f"   Elements: {len(blueprint.get('elements', []))} elements")
                
                # Print element types
                element_types = [el['type'] for el in blueprint.get('elements', [])]
                print(f"   Element types: {', '.join(set(element_types))}")
                
                return True
            else:
                print(f"❌ Generation failed: {result.get('error')}")
                return False
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Generation test failed: {e}")
        return False

def test_multiple_scenarios():
    """Test multiple design scenarios"""
    test_cases = [
        {
            "prompt": "Create a modern tech startup ad with bold headline",
            "platform": "meta",
            "format": "square"
        },
        {
            "prompt": "Design a vibrant fitness campaign with energetic colors",
            "platform": "meta",
            "format": "story"
        },
        {
            "prompt": "Make an elegant fashion brand announcement",
            "platform": "linkedin",
            "format": "landscape"
        },
        {
            "prompt": "Create a food delivery promotion with appetizing design",
            "platform": "google",
            "format": "square"
        }
    ]
    
    print("\n" + "="*60)
    print("Testing Multiple Design Scenarios")
    print("="*60)
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}/{len(test_cases)}")
        success = test_generation(**test_case)
        results.append(success)
    
    return results

def main():
    print("="*60)
    print("AdGenesis Design Blueprint Generation Test")
    print("="*60)
    
    # Test health
    if not test_health():
        print("\n❌ ML Service is not running. Please start it first:")
        print("   cd ml_pipeline && python3 serve_design.py")
        sys.exit(1)
    
    # Test single generation
    print("\n" + "="*60)
    print("Single Generation Test")
    print("="*60)
    test_generation("Create a professional business announcement ad")
    
    # Test multiple scenarios
    results = test_multiple_scenarios()
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Your ML pipeline is working perfectly.")
    else:
        print(f"\n⚠️  Some tests failed. Please check the logs.")
    
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()
