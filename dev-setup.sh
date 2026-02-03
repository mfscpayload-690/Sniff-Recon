#!/bin/bash
# Sniff-Recon Development Setup Script for Arch Linux
# This script sets up and runs Sniff-Recon in offline mode with Ollama

set -e  # Exit on error

echo "🚀 Sniff-Recon - Offline Mode Setup"
echo "===================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}❌ Ollama not found!${NC}"
    echo "Install with: curl -fsSL https://ollama.ai/install.sh | sh"
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python not found!${NC}"
    echo "Install with: sudo pacman -S python"
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found!${NC}"
    echo "Creating .env from .env.template..."
    cp .env.template .env
    echo -e "${GREEN}✅ .env created${NC}"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating Python virtual environment..."
    python -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing Python dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Check if Ollama model is downloaded
echo ""
echo "🤖 Checking Ollama model..."
if ollama list | grep -q "qwen2.5-coder:7b"; then
    echo -e "${GREEN}✅ qwen2.5-coder:7b model found${NC}"
else
    echo -e "${YELLOW}⚠️  Model qwen2.5-coder:7b not found${NC}"
    echo "Downloading model (this may take a while - ~4.7GB)..."
    ollama pull qwen2.5-coder:7b
    echo -e "${GREEN}✅ Model downloaded${NC}"
fi

# Check if Ollama is running
echo ""
echo "🔌 Checking Ollama daemon..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Ollama is running${NC}"
else
    echo -e "${YELLOW}⚠️  Ollama daemon not running${NC}"
    echo "Starting Ollama in background..."
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 2
    
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Ollama started successfully${NC}"
    else
        echo -e "${RED}❌ Failed to start Ollama${NC}"
        echo "Try manually: ollama serve"
        exit 1
    fi
fi

# Create output directory
mkdir -p output

# Final checks
echo ""
echo "✅ Setup Complete!"
echo ""
echo "📋 Configuration:"
echo "  • Mode: 🔒 Offline (Ollama)"
echo "  • Model: qwen2.5-coder:7b"
echo "  • Ollama URL: http://localhost:11434"
echo "  • Output Dir: ./output"
echo ""
echo "🚀 Starting Streamlit..."
echo ""
echo "=================================="
echo "Press Ctrl+C to stop"
echo "=================================="
echo ""

# Run Streamlit with auto-reload
streamlit run app.py \
    --server.runOnSave true \
    --server.port 8501 \
    --server.headless false
