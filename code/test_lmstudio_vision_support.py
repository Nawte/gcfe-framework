"""
Quick test: Does LM Studio support vision at all?
"""
import requests

# Test if the vision model is even loaded
response = requests.get("http://localhost:1234/v1/models")
models = response.json()

print("Loaded models:")
for model in models['data']:
    print(f"  - {model['id']}")

# Check if any vision model
has_vision = any('vl' in m['id'].lower() or 'vision' in m['id'].lower() or 'llava' in m['id'].lower() 
                 for m in models['data'])

if not has_vision:
    print("\n❌ NO VISION MODEL LOADED!")
    print("📌 Solution: Load a vision model in LM Studio:")
    print("   - qwen3.5-0.8b3-vl")
    print("   - llava-v1.6")
    print("   - bakllava")
else:
    print("\n✅ Vision model detected!")
    print("\n🔍 Testing if LM Studio supports vision API format...")
    
    # Try a simple vision request
    tiny_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="  # 1x1 red pixel
    
    request_data = {
        "model": models['data'][0]['id'],
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What color is this?"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{tiny_image}"}}
                ]
            }
        ],
        "max_tokens": 10
    }
    
    try:
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",
            json=request_data,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Vision API works!")
            print(f"   Response: {response.json()['choices'][0]['message']['content']}")
        else:
            print(f"❌ Vision API failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
            print("\n💡 LM Studio might not support OpenAI vision API format")
            print("   Try checking LM Studio docs or use a different approach")
    except Exception as e:
        print(f"❌ Request failed: {e}")
