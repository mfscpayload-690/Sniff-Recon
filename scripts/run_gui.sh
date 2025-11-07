#!/bin/bash
# Sniff Recon GUI Launcher Script
# This script activates the virtual environment and starts the GUI

echo "🔍 Sniff Recon - Network Packet Analyzer"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv_gui" ]; then
    echo "❌ Virtual environment 'venv_gui' not found!"
    echo "Please run the setup first:"
    echo "  python3 -m venv venv_gui"
    echo "  source venv_gui/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment and run GUI
echo "🔄 Activating virtual environment..."
source venv_gui/bin/activate

echo "🚀 Starting Sniff Recon GUI..."
echo "📱 The application will open in your web browser"
echo "⏹️  Press Ctrl+C to stop the application"
echo "=================================================="

# Run the GUI launcher
python start_gui.py
