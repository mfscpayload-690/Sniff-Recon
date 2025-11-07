#!/usr/bin/env python3
"""
Sniff Recon - Main Application Entry Point
Network Packet Analyzer with AI-Powered Analysis
"""
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the GUI
from ui.gui import main

if __name__ == "__main__":
    main()
