#!/usr/bin/env python3
"""
Sniff Recon GUI Launcher
Simple script to launch the Streamlit GUI application
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import scapy
        import pandas
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\n📦 Please install dependencies first:")
        print("pip install -r requirements.txt")
        return False

def main():
    """Launch the Sniff Recon GUI"""
    print("🔍 Sniff Recon - Network Packet Analyzer")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("sniff_recon_gui.py"):
        print("❌ Error: sniff_recon_gui.py not found!")
        print("Make sure you're in the Sniff-Recon directory.")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Launch Streamlit
    print("\n🚀 Starting Sniff Recon GUI...")
    print("📱 The application will open in your default web browser")
    print("🌐 URL: http://localhost:8501")
    print("\n⏹️  Press Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "sniff_recon_gui.py",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Sniff Recon GUI stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting GUI: {e}")
        print("Try running manually: streamlit run sniff_recon_gui.py")

if __name__ == "__main__":
    main()
