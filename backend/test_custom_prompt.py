#!/usr/bin/env python3
"""Test Flask API with custom prompts for moodboard generation"""

import requests
import json
import sys

def test_moodboard(prompt_text):
    """Test the Flask API endpoint with custom prompt"""
    
    url = "http://localhost:5000/analyze_emotion"
    
    test_data = {
        "text": prompt_text
    }
    
    try:
        print(f"🚀 Testing with prompt: '{prompt_text[:50]}...'")
        print("⏳ Generating moodboard (this may take 1-2 minutes)...")
        
        response = requests.post(url, json=test_data, timeout=120)  # Extended timeout for image extraction
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Moodboard generated successfully!")
            print(f"📁 Output path: {result.get('output_path', 'Not found')}")
            if 'session_log' in result:
                print(f"📝 Session: {result['session_log']}")
            return result
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - but moodboard might still be generating in background")
        print("💡 Check the server logs or moodboards folder for results")
        return None
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

if __name__ == "__main__":
    # Example prompts - you can modify these or add your own
    sample_prompts = [
        "Vibrant energy and excitement — electric blue, neon green, hot pink, and sunshine yellow. Dancing under disco lights, confetti falling, celebration balloons, party streamers, and pure happiness.",
        
        "Calm serenity and peace — soft lavender, gentle mint, warm cream, and sky blue. Meditation gardens, flowing water, peaceful stones, yoga mats, and tranquil moments.",
        
        "Bold confidence and power — deep burgundy, rich gold, midnight black, and crimson red. Luxury cars, city skylines, premium watches, leather jackets, and success stories.",
        
        "Natural harmony and growth — forest green, earth brown, sunshine yellow, and ocean blue. Hiking trails, blooming flowers, wooden cabins, fresh air, and outdoor adventures."
    ]
    
    if len(sys.argv) > 1:
        # Use command line argument as prompt
        custom_prompt = " ".join(sys.argv[1:])
        test_moodboard(custom_prompt)
    else:
        # Interactive mode - choose from samples or enter custom
        print("🎨 Moodboard Generator - Custom Prompt Test")
        print("\nChoose an option:")
        print("1. Vibrant energy (disco/celebration theme)")
        print("2. Calm serenity (meditation/peace theme)")  
        print("3. Bold confidence (luxury/power theme)")
        print("4. Natural harmony (nature/outdoor theme)")
        print("5. Enter custom prompt")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice in ['1', '2', '3', '4']:
            prompt = sample_prompts[int(choice) - 1]
            test_moodboard(prompt)
        elif choice == '5':
            custom_prompt = input("Enter your custom prompt: ").strip()
            if custom_prompt:
                test_moodboard(custom_prompt)
            else:
                print("❌ No prompt entered")
        else:
            print("❌ Invalid choice")
