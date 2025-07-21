#!/usr/bin/env python3
"""Test script to generate a moodboard directly"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from detect_important import parse_prompt, merge_prompt_with_spec, generate_moodboard
import json

def test_moodboard():
    """Test moodboard generation with a simple prompt"""
    
    # Test prompt
    test_prompt = "Pure joy in color — sunflower yellow, coral pink, sky blue, and mint green. Think laughter in the sun, picnic blankets, bubbles in the air, roller skates, and golden hour smiles."
    
    print(f"Testing with prompt: {test_prompt}")
    
    # Parse the prompt
    parsed_data = parse_prompt(test_prompt)
    print(f"Parsed data: {json.dumps(parsed_data, indent=2)}")
    
    # Use JOY/HAPPINESS as emotion
    emotion_label = "JOY/HAPPINESS"
    
    # Generate moodboard
    try:
        output_path, session_log = generate_moodboard(parsed_data, emotion_label)
        print(f"✅ Moodboard generated successfully!")
        print(f"📂 Output path: {output_path}")
        print(f"📋 Session log: {json.dumps(session_log, indent=2)}")
        
        # Check if file exists
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ File exists with size: {file_size} bytes")
        else:
            print("❌ Output file not found")
            
    except Exception as e:
        print(f"❌ Error generating moodboard: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_moodboard()
