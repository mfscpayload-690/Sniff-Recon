#!/usr/bin/env python3
"""
Multi-Agent AI Setup Script for Sniff Recon
Helps users configure multiple AI providers and test connections
"""

import os
import sys
import requests
from typing import Dict, List, Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

console = Console()

class AIProviderTester:
    """Test AI provider connections"""
    
    @staticmethod
    def test_groq(api_key: str) -> bool:
        """Test Groq API connection"""
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers=headers,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def test_openai(api_key: str) -> bool:
        """Test OpenAI API connection"""
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(
                "https://api.openai.com/v1/models",
                headers=headers,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def test_anthropic(api_key: str) -> bool:
        """Test Anthropic API connection"""
        try:
            headers = {
                "x-api-key": api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            payload = {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "Hello"}]
            }
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

def print_welcome():
    """Print welcome message"""
    welcome_text = """
    🔍 Sniff Recon Multi-Agent AI Setup
    
    This script will help you configure multiple AI providers for enhanced
    network analysis capabilities. You can set up one or more providers:
    
    • Groq (Fast, free tier available)
    • OpenAI (High quality, paid)
    • Anthropic Claude (Excellent for analysis)
    
    The system will automatically load-balance between active providers.
    """
    
    console.print(Panel(welcome_text, style="cyan bold", title="Welcome"))

def get_provider_info() -> Dict:
    """Get information about available providers"""
    return {
        "groq": {
            "name": "Groq",
            "description": "Fast inference with free tier",
            "signup_url": "https://console.groq.com/keys",
            "models": ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"],
            "free": True
        },
        "openai": {
            "name": "OpenAI",
            "description": "High-quality responses, paid service",
            "signup_url": "https://platform.openai.com/api-keys",
            "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
            "free": False
        },
        "anthropic": {
            "name": "Anthropic Claude",
            "description": "Excellent for detailed analysis",
            "signup_url": "https://console.anthropic.com/",
            "models": ["claude-3-sonnet-20240229", "claude-3-opus-20240229"],
            "free": False
        }
    }

def display_provider_info():
    """Display provider information table"""
    providers = get_provider_info()
    
    table = Table(title="🤖 Available AI Providers", show_header=True, header_style="bold magenta")
    table.add_column("Provider", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Free Tier", style="green")
    table.add_column("Sign Up", style="blue")
    
    for provider_id, info in providers.items():
        free_status = "✅ Yes" if info["free"] else "💳 Paid"
        table.add_row(
            info["name"],
            info["description"],
            free_status,
            info["signup_url"]
        )
    
    console.print(table)
    console.print()

def setup_provider(provider_id: str, provider_info: Dict) -> Optional[Dict]:
    """Set up a specific provider"""
    console.print(f"\n🔧 Setting up {provider_info['name']}", style="bold cyan")
    
    if not Confirm.ask(f"Do you want to configure {provider_info['name']}?"):
        return None
    
    console.print(f"You can get your API key from: {provider_info['signup_url']}")
    api_key = Prompt.ask(f"Enter your {provider_info['name']} API key", password=True)
    
    if not api_key or api_key.strip() == "":
        console.print("❌ No API key provided, skipping...", style="red")
        return None
    
    # Test the API key
    console.print(f"🔍 Testing {provider_info['name']} connection...")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(f"Testing {provider_info['name']}...", total=None)
        
        tester = AIProviderTester()
        if provider_id == "groq":
            is_valid = tester.test_groq(api_key)
        elif provider_id == "openai":
            is_valid = tester.test_openai(api_key)
        elif provider_id == "anthropic":
            is_valid = tester.test_anthropic(api_key)
        else:
            is_valid = False
        
        progress.stop()
    
    if is_valid:
        console.print(f"✅ {provider_info['name']} connection successful!", style="green")
        
        # Model selection
        default_model = provider_info["models"][0]
        if len(provider_info["models"]) > 1:
            console.print(f"Available models: {', '.join(provider_info['models'])}")
            model = Prompt.ask(f"Choose model", default=default_model)
        else:
            model = default_model
        
        return {
            "api_key": api_key,
            "model": model,
            "valid": True
        }
    else:
        console.print(f"❌ {provider_info['name']} connection failed. Please check your API key.", style="red")
        return None

def create_env_file(configurations: Dict):
    """Create .env file with configurations"""
    env_content = "# Sniff Recon - Multi-Agent AI Configuration\n"
    env_content += "# Generated by setup_multi_agent.py\n\n"
    
    # Add provider configurations
    for provider_id, config in configurations.items():
        if config:
            if provider_id == "groq":
                env_content += f"GROQ_API_KEY={config['api_key']}\n"
                env_content += f"GROQ_MODEL={config['model']}\n\n"
            elif provider_id == "openai":
                env_content += f"OPENAI_API_KEY={config['api_key']}\n"
                env_content += f"OPENAI_MODEL={config['model']}\n\n"
            elif provider_id == "anthropic":
                env_content += f"ANTHROPIC_API_KEY={config['api_key']}\n"
                env_content += f"ANTHROPIC_MODEL={config['model']}\n\n"
    
    # Add system configurations
    env_content += "# Multi-Agent System Configuration\n"
    env_content += "CHUNK_SIZE_MB=5\n"
    env_content += "MAX_PACKETS_PER_CHUNK=5000\n"
    env_content += "LOAD_BALANCING_STRATEGY=round_robin\n"
    env_content += "MAX_RETRIES=3\n"
    env_content += "REQUEST_TIMEOUT=60\n\n"
    
    # Add output configuration
    env_content += "# Output Configuration\n"
    env_content += "OUTPUT_DIR=output\n"
    env_content += "LOG_LEVEL=INFO\n"
    
    # Write to .env file
    with open(".env", "w") as f:
        f.write(env_content)
    
    console.print("✅ Configuration saved to .env file", style="green")

def install_dependencies():
    """Install required dependencies"""
    console.print("\n📦 Installing dependencies...", style="bold yellow")
    
    dependencies = [
        "aiohttp>=3.9.1",
        "openai>=1.12.0", 
        "anthropic>=0.18.1",
        "rich>=13.4.2"
    ]
    
    try:
        import subprocess
        for dep in dependencies:
            console.print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep], 
                                stdout=subprocess.DEVNULL, 
                                stderr=subprocess.DEVNULL)
        
        console.print("✅ All dependencies installed successfully!", style="green")
        return True
    except Exception as e:
        console.print(f"❌ Error installing dependencies: {e}", style="red")
        return False

def test_multi_agent_system():
    """Test the multi-agent system"""
    console.print("\n🧪 Testing multi-agent system...", style="bold cyan")
    
    try:
        from multi_agent_ai import multi_agent, get_active_providers
        
        providers = get_active_providers()
        
        if providers:
            console.print(f"✅ Multi-agent system loaded with {len(providers)} active providers:", style="green")
            for provider in providers:
                console.print(f"  • {provider}", style="cyan")
            return True
        else:
            console.print("⚠️ Multi-agent system loaded but no providers are active", style="yellow")
            return False
            
    except ImportError as e:
        console.print(f"❌ Error importing multi-agent system: {e}", style="red")
        return False
    except Exception as e:
        console.print(f"❌ Error testing multi-agent system: {e}", style="red")
        return False

def main():
    """Main setup function"""
    print_welcome()
    
    # Check if .env already exists
    if os.path.exists(".env"):
        if not Confirm.ask("❓ .env file already exists. Overwrite it?"):
            console.print("Setup cancelled.", style="yellow")
            return
    
    # Install dependencies first
    if not install_dependencies():
        console.print("❌ Failed to install dependencies. Please install manually:", style="red")
        console.print("pip install aiohttp openai anthropic rich")
        return
    
    # Display provider information
    display_provider_info()
    
    # Set up providers
    providers = get_provider_info()
    configurations = {}
    
    for provider_id, provider_info in providers.items():
        config = setup_provider(provider_id, provider_info)
        configurations[provider_id] = config
    
    # Check if at least one provider was configured
    valid_providers = sum(1 for config in configurations.values() if config and config.get("valid"))
    
    if valid_providers == 0:
        console.print("❌ No valid providers configured. Setup incomplete.", style="red")
        return
    
    # Create .env file
    create_env_file(configurations)
    
    # Test the system
    if test_multi_agent_system():
        console.print("\n🎉 Setup completed successfully!", style="bold green")
        console.print("\nNext steps:", style="bold cyan")
        console.print("1. Run: python enhanced_cli_ai.py -f your_pcap_file.pcap -i")
        console.print("2. Or try: python enhanced_cli_ai.py --help")
        console.print("\nFor large files (>50MB), the system will automatically chunk the data for efficient processing.")
    else:
        console.print("\n⚠️ Setup completed but system test failed. Check your configuration.", style="yellow")

if __name__ == "__main__":
    main()
