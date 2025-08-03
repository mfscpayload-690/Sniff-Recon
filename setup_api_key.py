#!/usr/bin/env python3
"""
Setup script for Groq API Key

This script helps users set up their Groq API key for the Sniff Recon application.
"""

import os
import requests
from dotenv import load_dotenv

def test_api_key(api_key):
    """Test if the API key is valid"""
    try:
        response = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )
        return response.status_code == 200
    except Exception:
        return False

def main():
    print("🔐 Groq API Key Setup for Sniff Recon")
    print("=" * 50)
    
    load_dotenv()
    current_key = os.getenv("GROQ_API_KEY")
    
    if current_key and "gsk_" in current_key:
        print("🔍 Found existing Groq API key.")
        if test_api_key(current_key):
            print("✅ Your current API key is valid!")
            return
        else:
            print("❌ Your current API key is invalid.")
    
    print("\n📋 To use AI-powered analysis, you need a Groq API key.")
    print("\n🔗 Get your free API key from: https://console.groq.com/keys")
    
    print("\n" + "=" * 50)
    
    new_key = input("\n🤖 Enter your Groq API key (or press Enter to skip): ").strip()
    
    if not new_key:
        print("\n⚠️ No API key provided. AI features will use local analysis.")
        return
    
    print("\n🔍 Testing API key...")
    if test_api_key(new_key):
        print("✅ API key is valid!")
        
        env_content = f"GROQ_API_KEY={new_key}\nMODEL_NAME=llama3-8b-8192\n"
        
        with open(".env", "w") as f:
            f.write(env_content)
        
        print("✅ API key saved to .env file!")
        print("\n🚀 You can now use AI-powered analysis in Sniff Recon!")
        
    else:
        print("❌ Invalid API key. Please check your key and try again.")
        print("💡 Make sure you copied the entire token from Groq.")

if __name__ == "__main__":
    main() 