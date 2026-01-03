import requests
import json

# Test modern design generation
test_prompts = [
    {
        "prompt": "AI-powered software for modern businesses",
        "platform": "instagram",
        "format": "square",
        "tone": "professional",
        "industry": "technology"
    },
    {
        "prompt": "Summer fashion sale - up to 70% off",
        "platform": "instagram",
        "format": "square",
        "tone": "vibrant",
        "industry": "fashion"
    },
    {
        "prompt": "Premium gym membership - transform your body",
        "platform": "instagram",
        "format": "square",
        "tone": "energetic",
        "industry": "fitness"
    }
]

print("�� Testing MODERN Design Generation")
print("=" * 60)

for i, request_data in enumerate(test_prompts, 1):
    print(f"\n📍 Test {i}: {request_data['prompt'][:50]}...")
    
    response = requests.post(
        "http://localhost:8001/generate",
        json=request_data,
        timeout=120
    )
    
    if response.status_code == 200:
        result = response.json()
        
        # Show design details
        blueprint = result.get("design_blueprint", {})
        metadata = blueprint.get("metadata", {})
        elements = blueprint.get("elements", [])
        
        print(f"   ✅ Generated: {metadata.get('design_style', 'N/A')}")
        print(f"   📐 Dimensions: {metadata.get('width')}x{metadata.get('height')}")
        print(f"   🎨 Elements: {len(elements)} total")
        print(f"   📝 Headline: {blueprint.get('headline', '')[:60]}")
        print(f"   💬 Subheadline: {blueprint.get('subheadline', '')[:60]}")
        print(f"   🔘 CTA: {blueprint.get('cta_text', '')}")
        
        # Count element types
        text_count = sum(1 for e in elements if e.get('type') == 'text')
        shape_count = sum(1 for e in elements if e.get('type') == 'shape')
        button_count = sum(1 for e in elements if e.get('type') == 'cta_button')
        
        print(f"   🔢 Breakdown: {text_count} text, {shape_count} shapes, {button_count} buttons")
    else:
        print(f"   ❌ Error: {response.status_code}")
        print(f"   {response.text}")

print("\n" + "=" * 60)
print("✨ Modern design system test complete!")
