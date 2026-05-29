"""
Test LM Studio with the ACTUAL user image
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from core.vision_processor import VisionProcessor
import requests

# Load the user's actual image
vision_proc = VisionProcessor()
image_path = r"C:\Users\shake\Downloads\fc4d2b51dfaa9867.jpg"

print(f"Loading image: {image_path}")
data_url = vision_proc.process_image(image_path)

if not data_url:
    print("❌ Failed to load image")
    sys.exit(1)

print(f"✅ Image loaded: {len(data_url)} chars")
print(f"   Format: {data_url[:50]}...")

# Now test with LM Studio
print("\nTesting with LM Studio...")

request_data = {
    "model": "qwen3.5-0.8b/qwen3.5-0.8b/qwen3.5-0.8b3.5-9b 27B-35b-a3b",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What do you see in this image?"},
                {"type": "image_url", "image_url": {"url": data_url}}
            ]
        }
    ],
    "max_tokens": 100
}

print(f"Request size: ~{len(str(request_data)) / 1024:.1f} KB")

try:
    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        json=request_data,
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()
        content = result['choices'][0]['message']['content']
        print(f"\n✅ SUCCESS!")
        print(f"Skippy sees: {content}")
    else:
        print(f"\n❌ FAILED: {response.status_code}")
        print(f"Error: {response.text}")
        
        # Try to diagnose
        if "Failed to load" in response.text:
            print("\n💡 Diagnosis: LM Studio cannot process this image format")
            print("   Possible issues:")
            print("   1. Image too large (try reducing quality in vision_processor.py)")
            print("   2. JPEG format issue (try converting to PNG)")
            print("   3. LM Studio version doesn't support large images")
except Exception as e:
    print(f"\n❌ Request failed: {e}")
