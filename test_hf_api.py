#!/usr/bin/env python3
"""
Test Hugging Face API Key

This script helps you test if your Hugging Face API key is valid.
"""

import requests
import os
from dotenv import load_dotenv

def test_api_key(api_key):
    """Test if the API key is valid"""
    try:
        print(f"🔍 Testing API key: {api_key[:10]}...")
        response = requests.get(
            "https://huggingface.co/api/whoami",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )
        
        if response.status_code == 200:
            user_info = response.json()
            print("✅ API key is valid!")
            print(f"👤 User: {user_info.get('name', 'Unknown')}")
            print(f"📧 Email: {user_info.get('email', 'Unknown')}")
            return True
        else:
            print(f"❌ API key is invalid (Status: {response.status_code})")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API key: {e}")
        return False

def main():
    print("🔐 Hugging Face API Key Tester")
    print("=" * 40)
    
    # Load from .env file
    load_dotenv()
    env_key = os.getenv("HUGGINGFACE_API_KEY")
    
    if env_key:
        print(f"📁 Found API key in .env file: {env_key[:10]}...")
        if test_api_key(env_key):
            print("\n🎉 Your .env file contains a valid API key!")
            return
        else:
            print("\n⚠️  The API key in your .env file is invalid.")
    
    # Prompt for manual input
    print("\n" + "=" * 40)
    print("🔗 Get a free API key from: https://huggingface.co/settings/tokens")
    print("1. Go to the link above")
    print("2. Click 'New token'")
    print("3. Give it a name (e.g., 'Sniff Recon')")
    print("4. Select 'Read' role")
    print("5. Copy the generated token")
    
    manual_key = input("\n🤖 Enter your API key to test: ").strip()
    
    if manual_key:
        if test_api_key(manual_key):
            print("\n✅ This API key is valid!")
            print("💡 You can now update your .env file with this key.")
        else:
            print("\n❌ This API key is invalid. Please check and try again.")
    else:
        print("\n⚠️  No API key provided.")

if __name__ == "__main__":
    main() 