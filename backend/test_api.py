#!/usr/bin/env python3
"""Test Flask API for moodboard generation"""

import requests
import json

def test_api():
    """Test the Flask API endpoint"""
    
    url = "http://localhost:5000/analyze_emotion"
    
    test_data = {
        "text": "Pure joy in color — sunflower yellow, coral pink, sky blue, and mint green. Think laughter in the sun, picnic blankets, bubbles in the air, roller skates, and golden hour smiles."
    }
    
    try:
        print("🚀 Testing Flask API...")
        response = requests.post(url, json=test_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API call successful!")
            print(f"📊 Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ API call failed with status {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask server. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
