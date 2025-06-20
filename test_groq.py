#!/usr/bin/env python3
"""
Simple test script to verify Groq API integration
"""

import requests
import json

def test_groq_api():
    """Test Groq API with a simple request."""
    
    # You'll need to set your Groq API key here
    api_key = input("Enter your Groq API key: ").strip()
    
    if not api_key:
        print("No API key provided. Exiting.")
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Please respond with a simple greeting."}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    try:
        print("Sending request to Groq API...")
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Response structure:")
            print(json.dumps(result, indent=2))
            
            # Try to extract content
            if "choices" in result and len(result["choices"]) > 0:
                choice = result["choices"][0]
                if "message" in choice:
                    message = choice["message"]
                    content = message.get("content", "")
                    print(f"\nExtracted content: {content}")
                else:
                    print("No message found in choice")
            else:
                print("No choices found in response")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_groq_api() 