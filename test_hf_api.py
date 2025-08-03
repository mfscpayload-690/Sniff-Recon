#!/usr/bin/env python3
"""
Sniff Recon - PCAP Analysis with OpenAI API

This script provides OpenAI API integration for analyzing PCAP logs
with natural language queries and AI-powered insights.
"""

import os
import sys
import time
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OpenAIAPIError(Exception):
    """Custom exception for OpenAI API errors"""
    pass

class SniffReconAI:
    """AI-powered PCAP analysis using OpenAI API"""
    
    def __init__(self):
        """Initialize the AI client with API credentials"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
        self.base_url = "https://api.openai.com/v1/chat/completions"
        
        if not self.api_key:
            raise OpenAIAPIError("OPENAI_API_KEY not found in .env file")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def test_connection(self) -> bool:
        """
        Test the OpenAI API connection with a simple query
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            print(f"🔍 Testing OpenAI API connection...")
            print(f"🤖 Using model: {self.model_name}")
            print(f"🔑 API Key: {self.api_key[:10]}...")
            
            response = self.ask_ai("Hello! Please respond with 'Connection successful' if you can see this message.")
            
            if "Connection successful" in response:
                print("✅ OpenAI API connection successful!")
                return True
            else:
                print("⚠️  API responded but not as expected")
                return False
                
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False
    
    def ask_ai(self, prompt: str, max_retries: int = 3) -> str:
        """
        Send a query to OpenAI and get a response
        
        Args:
            prompt (str): The user's query/prompt
            max_retries (int): Maximum number of retry attempts
            
        Returns:
            str: AI response text
            
        Raises:
            OpenAIAPIError: For API-related errors
        """
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        for attempt in range(max_retries):
            try:
                print(f"🤖 Sending query to {self.model_name}...")
                response = requests.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                
                # Handle different HTTP status codes
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result["choices"][0]["message"]["content"]
                    print("✅ AI response received successfully!")
                    return ai_response
                    
                elif response.status_code == 401:
                    raise OpenAIAPIError("Invalid API key. Please check your OPENAI_API_KEY in .env file")
                    
                elif response.status_code == 429:
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) * 5  # Exponential backoff
                        print(f"⏳ Rate limited. Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise OpenAIAPIError("Rate limit exceeded. Please try again later.")
                        
                elif response.status_code == 404:
                    raise OpenAIAPIError(f"Model '{self.model_name}' not found. Please check your MODEL_NAME in .env file")
                    
                else:
                    error_msg = f"API request failed with status {response.status_code}: {response.text}"
                    raise OpenAIAPIError(error_msg)
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"⏳ Request timeout. Retrying... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(2)
                    continue
                else:
                    raise OpenAIAPIError("Request timeout after multiple attempts")
                    
            except requests.exceptions.ConnectionError:
                raise OpenAIAPIError("Network connection error. Please check your internet connection.")
                
            except Exception as e:
                raise OpenAIAPIError(f"Unexpected error: {str(e)}")
        
        raise OpenAIAPIError("Failed to get response after maximum retries")

def create_env_template():
    """Create a template .env file if it doesn't exist"""
    env_content = """# Sniff Recon - OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys

OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-3.5-turbo

# Optional: Alternative models you can use
# MODEL_NAME=gpt-4
# MODEL_NAME=gpt-4-turbo-preview
"""
    
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_content)
        print("📝 Created .env template file")
        print("🔑 Please add your OpenAI API key to the .env file")
        return False
    return True

def main():
    """Main function to test and demonstrate the AI integration"""
    print("🔍 Sniff Recon - OpenAI API Integration")
    print("=" * 50)
    
    # Check if .env exists and has required variables
    if not create_env_template():
        return
    
    try:
        # Initialize AI client
        ai_client = SniffReconAI()
        
        # Test connection
        if not ai_client.test_connection():
            print("❌ Failed to establish connection with OpenAI API")
            return
        
        print("\n" + "=" * 50)
        print("🎯 AI Integration Ready!")
        print("=" * 50)
        
        # Interactive mode
        while True:
            print("\n💬 Enter your query (or 'quit' to exit):")
            user_input = input("> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            try:
                response = ai_client.ask_ai(user_input)
                print(f"\n🤖 AI Response:\n{response}")
            except OpenAIAPIError as e:
                print(f"❌ Error: {e}")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
    
    except OpenAIAPIError as e:
        print(f"❌ Initialization error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you have a valid OpenAI API key")
        print("2. Check your .env file contains OPENAI_API_KEY")
        print("3. Verify your internet connection")
        print("4. Ensure you have sufficient API credits")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()

# =============================================================================
# FUTURE AGENTIC IMPROVEMENTS - Add these features later:
# =============================================================================
"""
🎯 PCAP Analysis Features to Add:

1. PCAP File Processing:
   - Load and parse PCAP files using scapy or pyshark
   - Extract packet metadata (timestamps, protocols, IPs, ports)
   - Generate summary statistics

2. Natural Language PCAP Queries:
   - "Show me all HTTP requests to suspicious domains"
   - "Find packets with unusual port activity"
   - "Analyze traffic patterns between 10:00 AM and 2:00 PM"
   - "Identify potential security threats in this capture"

3. AI-Powered Analysis:
   - Automatic threat detection and classification
   - Anomaly detection in network traffic
   - Behavioral analysis of network flows
   - Security incident correlation

4. Advanced Features:
   - Real-time packet capture analysis
   - Network topology mapping
   - Protocol-specific analysis (HTTP, DNS, TLS, etc.)
   - Export findings to reports (PDF, JSON, CSV)
   - Integration with threat intelligence feeds
   - Custom rule-based filtering
   - Machine learning model training on PCAP data

5. GUI Enhancements:
   - Interactive packet viewer
   - Network flow diagrams
   - Real-time traffic visualization
   - Filter and search capabilities
   - Export and sharing features

6. CLI Features:
   - Batch processing of multiple PCAP files
   - Command-line arguments for automation
   - Scriptable analysis workflows
   - Integration with other security tools

7. Data Processing:
   - PCAP file compression and optimization
   - Database storage for large captures
   - Incremental analysis capabilities
   - Data retention policies

8. Security Features:
   - Encrypted storage of sensitive data
   - Access control and authentication
   - Audit logging
   - Compliance reporting (GDPR, HIPAA, etc.)
""" 