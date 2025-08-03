#!/usr/bin/env python3
"""
Setup script for Hugging Face API Key

This script helps users set up their Hugging Face API key for the Sniff Recon application.
"""

import os
import requests
from dotenv import load_dotenv

def test_api_key(api_key):
    """Test if the API key is valid"""
    try:
        response = requests.get(
            "https://huggingface.co/api/whoami",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )
        return response.status_code == 200
    except Exception:
        return False

def main():
    print("🔐 Hugging Face API Key Setup for Sniff Recon")
    print("=" * 50)
    
    # Load existing .env file
    load_dotenv()
    current_key = os.getenv("HUGGINGFACE_API_KEY")
    
    if current_key:
        print(f"🔍 Found existing API key: {current_key[:10]}...")
        if test_api_key(current_key):
            print("✅ Your current API key is valid!")
            return
        else:
            print("❌ Your current API key is invalid.")
    
    print("\n📋 To use AI-powered analysis, you need a Hugging Face API key.")
    print("\n🔗 Get your free API key:")
    print("1. Go to https://huggingface.co/settings/tokens")
    print("2. Click 'New token'")
    print("3. Give it a name (e.g., 'Sniff Recon')")
    print("4. Select 'Read' role")
    print("5. Copy the generated token")
    
    print("\n" + "=" * 50)
    
    # Get new API key from user
    new_key = input("\n🤖 Enter your Hugging Face API key (or press Enter to skip): ").strip()
    
    if not new_key:
        print("\n⚠️  No API key provided. AI features will use local analysis.")
        return
    
    # Test the new key
    print("\n🔍 Testing API key...")
    if test_api_key(new_key):
        print("✅ API key is valid!")
        
        # Update .env file
        env_content = f"HUGGINGFACE_API_KEY={new_key}\n"
        
        with open(".env", "w") as f:
            f.write(env_content)
        
        print("✅ API key saved to .env file!")
        print("\n🚀 You can now use AI-powered analysis in Sniff Recon!")
        
    else:
        print("❌ Invalid API key. Please check your key and try again.")
        print("💡 Make sure you copied the entire token from Hugging Face.")

if __name__ == "__main__":
    main() 