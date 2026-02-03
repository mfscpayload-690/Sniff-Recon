# Setup Guide

Complete installation guide for Sniff-Recon network packet analyzer.

---

## Prerequisites

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **RAM** | 4GB | 8-16GB (Ollama: 16GB) |
| **Disk** | 2GB | 10GB+ (with Ollama models) |
| **CPU** | 2 cores | 4+ cores |
| **GPU** | None | NVIDIA/AMD (faster Ollama) |
| **OS** | Linux, macOS, Windows | Linux (best performance) |

### Software Requirements

- **Python**: 3.11+ (3.12 recommended)
- **Docker** (optional): 24.0+ with Docker Compose
- **Ollama** (optional, for offline mode): Latest version
- **Git**: For cloning the repository

---

## Installation Methods

### Method 1: Offline Mode (Ollama) 🔒

**Best for**: Privacy-sensitive environments, classified traffic, air-gapped networks

#### Step 1: Install Ollama

**Linux**:

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**macOS**:

```bash
brew install ollama
```

**Windows**:
Download from [ollama.ai/download](https://ollama.ai/download)

#### Step 2: Download Sniff-Recon

```bash
git clone https://github.com/mfscpayload-690/Sniff-Recon.git
cd Sniff-Recon
```

#### Step 3: Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Configure Ollama

```bash
# Start Ollama daemon
ollama serve &

# Download model (choose one)
ollama pull qwen2.5-coder:7b     # Recommended (8GB RAM)
# ollama pull llama3:8b           # Alternative
# ollama pull codellama:13b       # More accurate (16GB RAM)

# Verify installation
ollama list
```

#### Step 5: Configure Environment

```bash
# Copy template
cp .env.template .env

# Edit .env
nano .env  # or your editor
```

Set these values:

```bash
OLLAMA_ENABLED=true
OLLAMA_MODEL=qwen2.5-coder:7b
OLLAMA_BASE_URL=http://localhost:11434

# Placeholder cloud keys (prevents errors)
GROQ_API_KEY=offline_mode
OPENAI_API_KEY=offline_mode
ANTHROPIC_API_KEY=offline_mode
GOOGLE_API_KEY=offline_mode
XAI_API_KEY=offline_mode
```

#### Step 6: Run Sniff-Recon

```bash
streamlit run app.py
```

Open browser: **<http://localhost:8501>**

---

### Method 2: Cloud AI Mode (Docker) ☁️

**Best for**: Maximum AI quality, easier deployment

#### Step 1: Install Docker

**Linux**:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose

# Arch Linux
sudo pacman -S docker docker-compose
sudo systemctl enable --now docker
```

**macOS/Windows**:
Download [Docker Desktop](https://www.docker.com/products/docker-desktop/)

#### Step 2: Get API Keys

Sign up for **at least one** provider (Groq recommended for free tier):

- [Groq](https://console.groq.com) - Free tier, fast
- [OpenAI](https://platform.openai.com/api-keys) - Paid, best quality  
- [Google Gemini](https://makersuite.google.com/app/apikey) - Free tier
- [Anthropic](https://console.anthropic.com) - Paid, Claude
- [xAI](https://console.x.ai) - Paid, Grok

#### Step 3: Clone and Configure

```bash
git clone https://github.com/mfscpayload-690/Sniff-Recon.git
cd Sniff-Recon

# Create .env file
cp .env.template .env

# Edit .env and add API keys
nano .env
```

Example `.env`:

```bash
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
GOOGLE_API_KEY=AIzaxxxxxxxxxxxxx
XAI_API_KEY=xai-xxxxxxxxxxxxx
```

#### Step 4: Deploy with Docker

```bash
docker-compose up -d
```

#### Step 5: Verify Deployment

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f

# Access app
```

Open browser: **<http://localhost:8501>**

---

### Method 3: Local Python (Development) 💻

**Best for**: Development, customization, debugging

#### Prerequisites

```bash
# Install system dependencies (Linux/Debian-based)
sudo apt install python3.11 python3-pip python3-venv libpcap-dev tshark

# Arch Linux
sudo pacman -S python python-pip tcpdump wireshark-cli

# macOS
brew install python@3.11 wireshark
```

#### Installation

```bash
# Clone repository
git clone https://github.com/mfscpayload-690/Sniff-Recon.git
cd Sniff-Recon

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

#### Configuration

Choose **either** Ollama (offline) **or** Cloud AI:

**For Ollama**:

```bash
cp .env.template .env
# Edit .env: OLLAMA_ENABLED=true
# Start Ollama: ollama serve &
```

**For Cloud AI**:

```bash
cp .env.template .env
# Edit .env: Add API keys
```

#### Run

```bash
# Production mode
streamlit run app.py

# Development mode (auto-reload)
streamlit run app.py --server.runOnSave true

# Custom port
streamlit run app.py --server.port 8080
```

---

## Post-Installation

### Verify Installation

#### 1. Check Python Dependencies

```python
# Test imports
python -c "import streamlit, scapy, pandas; print('✅ Dependencies OK')"
```

#### 2. Test Parsers

```python
from src.parsers.pcap_parser import parse_pcap
# Should import without errors
```

#### 3. Check AI Providers

**For Ollama**:

```bash
curl http://localhost:11434/api/tags
# Should return JSON with models
```

**For Cloud AI**:

```python
from src.ai.multi_agent_ai import get_active_providers
providers = get_active_providers()
print(f"Active providers: {providers}")
```

### Get Test Data

```bash
# Create test directory
mkdir -p test-data

# Download sample PCAPs
cd test-data
wget https://wiki.wireshark.org/uploads/__moin_import__/attachments/SampleCaptures/http.cap
wget https://wiki.wireshark.org/uploads/__moin_import__/attachments/SampleCaptures/dns.cap
```

---

## Configuration Reference

### Environment Variables

See [.env.template](../.env.template) for all options. Key settings:

```bash
# === AI Providers ===
GROQ_API_KEY=sk-...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
GOOGLE_API_KEY=AIza...
XAI_API_KEY=xai-...

# === Ollama (Offline) ===
OLLAMA_ENABLED=false
OLLAMA_MODEL=qwen2.5-coder:7b
OLLAMA_BASE_URL=http://localhost:11434

# === File Processing ===
MAX_FILE_SIZE_MB=200
CHUNK_SIZE_MB=5
MAX_PACKETS_PER_CHUNK=5000

# === Load Balancing ===
LOAD_BALANCING_STRATEGY=weighted
GROQ_WEIGHT=30
OPENAI_WEIGHT=25

# === Security ===
AI_RATE_LIMIT_PER_MINUTE=30
ALLOWED_EXTENSIONS=pcap,pcapng,csv,txt

# === Output ===
OUTPUT_DIR=./output
```

---

## Platform-Specific Notes

### Linux (Arch)

```bash
# Install all dependencies
sudo pacman -S python python-pip tcpdump wireshark-cli docker docker-compose

# Enable Docker
sudo systemctl enable --now docker
sudo usermod -aG docker $USER  # Reboot after this

# For Ollama
yay -S ollama  # or: curl -fsSL https://ollama.ai/install.sh | sh
```

### macOS

```bash
# Install via Homebrew
brew install python@3.11 wireshark ollama

# Start Ollama
brew services start ollama
```

### Windows (WSL2)

Recommended: Use WSL2 (Ubuntu) for best compatibility

```bash
# Inside WSL2
sudo apt update
sudo apt install python3.11 python3-venv python3-pip libpcap-dev tshark

# Install Ollama (Linux method)
curl -fsSL https://ollama.ai/install.sh | sh
```

---

## Automated Setup (Arch Linux)

For Arch Linux users, use the provided setup script:

```bash
cd Sniff-Recon
./dev-setup.sh
```

This script:

- ✅ Checks Ollama installation
- ✅ Creates Python venv
- ✅ Installs dependencies
- ✅ Downloads AI model
- ✅ Starts Ollama daemon
- ✅ Launches Streamlit

---

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'scapy'`  
**Fix**: Activate venv and reinstall dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Issue**: `Cannot connect to Ollama`  
**Fix**: Start Ollama daemon

```bash
ollama serve &
```

**Issue**: `Permission denied` (Docker)  
**Fix**: Add user to docker group

```bash
sudo usermod -aG docker $USER
# Logout and login again
```

**Issue**: Port 8501 already in use  
**Fix**: Use different port

```bash
streamlit run app.py --server.port 8080
```

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more solutions.

---

## Next Steps

1. ✅ Upload a test PCAP file
2. ✅ Select AI provider (Ollama or Cloud)
3. ✅ Ask a test query: "What are the top 5 IPs?"
4. ✅ Explore packet inspection features
5. ✅ Read [OLLAMA.md](OLLAMA.md) for offline mode details

---

**Need Help?**

- [GitHub Issues](https://github.com/mfscpayload-690/Sniff-Recon/issues)
- [Documentation](../README.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
