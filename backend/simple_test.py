#!/usr/bin/env python3
"""Simple test for different prompts - just change the text and run"""

import requests
import json

# ✨ CHANGE THIS TEXT TO TEST DIFFERENT PROMPTS ✨
import requests

# Test prompt to trigger PEACE/SERENITY emotion (should use Peace.svg)
test_prompt = "calm meditation and tranquility — soft blue, gentle white, natural green. peaceful mountains, zen garden, quiet lake, serene forest, harmony."

print(f"🚀 Testing prompt: '{test_prompt[:60]}...'")
print("⏳ Generating moodboard (should use Peace.svg for top-left)...")

try:
    response = requests.post("http://127.0.0.1:5000/analyze_emotion", 
                           json={"prompt": test_prompt},
                           timeout=120)
    
    if response.status_code == 200:
        print("✅ SUCCESS! Moodboard generated!")
        print("📁 File: Check moodboards folder")
        
        # Check what emotion was mapped
        data = response.json()
        if 'emotion' in data:
            print(f"🎯 Mapped to emotion: {data['emotion']}")
            print(f"🖼️  Should have Peace.svg in top-left corner!")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")

# Test data
data = {"text": test_prompt}

try:
    print(f"🚀 Testing prompt: '{test_prompt[:60]}...'")
    print("⏳ Generating moodboard (images will download from Pinterest)...")
    
    # The API call
    response = requests.post("http://localhost:5000/analyze_emotion", 
                           json=data, 
                           timeout=180)  # 3 min timeout
    
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS! Moodboard generated!")
        print(f"📁 File: {result.get('output_path', 'Check moodboards folder')}")
    else:
        print(f"Status: {response.status_code}")
        print("💡 Check the server logs - images might still be downloading!")
        
except Exception as e:
    print(f"Request issue: {e}")
    print("💡 The moodboard might still be generating - check the backend folder!")
