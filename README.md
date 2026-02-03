<div align="center">

# 🔍 Sniff-Recon

### AI-Powered Network Packet Analysis Platform

**Analyze network traffic with state-of-the-art AI - Cloud or 100% Offline**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-yellow?logo=buymeacoffee)](https://buymeacoffee.com/mfscpayload690)

[Features](#-key-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

---

</div>

## 📖 Overview

**Sniff-Recon** is a professional-grade network packet analyzer that combines traditional packet analysis with cutting-edge AI technology. Built for security researchers, SOC teams, and network engineers, it transforms complex PCAP data into actionable insights through natural language queries.

### 🎯 Why Sniff-Recon?

- **🔒 Privacy-First**: Full offline mode with local LLMs (Ollama) - no data leaves your machine
- **🤖 Multi-Provider AI**: Support for 6 AI providers (Groq, OpenAI, Anthropic, Google Gemini, xAI, Ollama)
- **📊 Smart Analysis**: Automatic suspicious packet detection and threat clustering
- **🎨 Modern UI**: Beautiful cyberpunk-themed Streamlit interface
- **🐳 Deploy Anywhere**: Docker-ready, works on Linux/Windows/macOS
- **🚀 Scalable**: Handle large PCAPs (up to 200MB) with intelligent chunking

---

## ✨ Key Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Multi-Format Support** | PCAP, PCAPNG, CSV, TXT log files |
| **AI-Powered Analysis** | Natural language queries: "Show me all SYN floods" |
| **Offline Mode** | 🔒 100% local analysis with Ollama (no external APIs) |
| **Cloud AI Support** | Groq, OpenAI, Anthropic, Google Gemini, xAI (Grok) |
| **Load Balancing** | Intelligent query distribution across AI providers |
| **Packet Inspection** | Layer-by-layer protocol analysis (Ethernet → Application) |
| **Threat Detection** | Automatic suspicious pattern identification |
| **Export Capabilities** | JSON, CSV, PDF reports |
| **Large File Handling** | Chunking strategy for files up to 200MB |
| **Docker Deployment** | One-command containerized setup |

### AI Analysis Modes

<table>
<tr>
<th>☁️ Cloud Mode</th>
<th>🔒 Offline Mode</th>
</tr>
<tr>
<td>

- **Providers**: Groq, OpenAI, Anthropic, Google Gemini, xAI
- **Benefits**: Fast, high-quality responses
- **Use Case**: General analysis, non-sensitive traffic
- **Cost**: API usage fees (Groq has free tier)

</td>
<td>

- **Provider**: Ollama (Local LLM)
- **Benefits**: 100% privacy, no API costs, air-gapped
- **Use Case**: Classified/sensitive traffic, GDPR compliance
- **Hardware**: 8-16GB RAM recommended

</td>
</tr>
</table>

---

## 🚀 Quick Start

> **Note**: Sniff-Recon is a **local-only** tool. All analysis runs on your machine for maximum privacy and control.

### Option 1: 🔒 Offline Mode (Ollama - Recommended)

**Best for**: Privacy-sensitive analysis, classified traffic, air-gapped networks

```bash
# 1. Clone repository
git clone https://github.com/mfscpayload-690/Sniff-Recon.git
cd Sniff-Recon

# 2. Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh  # Linux
# brew install ollama  # macOS

# 3. Start Ollama and download model
ollama serve &
ollama pull qwen2.5-coder:7b

# 4. Configure environment
cp .env.template .env
# Edit .env: Set OLLAMA_ENABLED=true

# 5. Run automated setup
./dev-setup.sh

# Access at http://localhost:8501
```

**System Requirements**:

- **RAM**: 8GB minimum (16GB recommended)
- **Disk**: 5GB for model + dependencies
- **OS**: Linux, macOS, Windows (WSL2)

---

### Option 2: ☁️ Cloud AI Mode (Docker)

**Best for**: Maximum AI quality, faster responses

```bash
# 1. Clone repository
git clone https://github.com/mfscpayload-690/Sniff-Recon.git
cd Sniff-Recon

# 2. Configure API keys
cp .env.template .env
# Edit .env and add your API keys:
#   GROQ_API_KEY=sk-...        (Free tier available)
#   OPENAI_API_KEY=sk-...
#   ANTHROPIC_API_KEY=sk-...
#   GOOGLE_API_KEY=...
#   XAI_API_KEY=...

# 3. Run with Docker
docker-compose up -d

# Access at http://localhost:8501
```

**Get Free API Keys**:

- [Groq](https://console.groq.com) - Fast inference, free tier ⭐
- [OpenAI](https://platform.openai.com/api-keys) - Best quality
- [Google Gemini](https://makersuite.google.com/app/apikey) - Free tier
- [Anthropic](https://console.anthropic.com) - Claude models
- [xAI](https://console.x.ai) - Grok

---

### Option 3: 💻 Local Python (Development)

**Best for**: Development, testing, customization

```bash
git clone https://github.com/mfscpayload-690/Sniff-Recon.git
cd Sniff-Recon

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Configure .env (Ollama or Cloud AI)
cp .env.template .env

# Run the app
streamlit run app.py

# Access at http://localhost:8501
```

---

## 📚 Usage Guide

### 1. Upload Packet Capture

Supported formats:

- **PCAP/PCAPNG**: Standard packet captures (Wireshark, tcpdump)
- **CSV**: Exported packet data with IP/port columns
- **TXT**: Structured logs (IP, protocol, ports)

### 2. Select AI Provider

**For Sensitive Data** (Offline):

1. Select **"Ollama (Local)"** from dropdown
2. Look for 🔒 **OFFLINE** badge
3. All analysis runs on your machine

**For General Analysis** (Cloud):

1. Select **"Auto (Load Balanced)"** for automatic distribution
2. Or choose specific provider (Groq, OpenAI, etc.)

### 3. Analyze with Natural Language

Ask questions like:

- "What are the top 5 source IP addresses?"
- "Show me all SYN flood attempts"
- "Identify suspicious DNS queries"
- "Analyze HTTP traffic patterns"
- "Find potential port scans"

### 4. Inspect Packets

- **Protocol Stats**: Packet counts, IP distributions
- **Packet Table**: Interactive AgGrid with filtering
- **Layer Inspector**: Ethernet → IP → TCP/UDP → Application
- **Hex Dump**: Raw packet data view

### 5. Export Results

- **JSON**: Structured analysis data
- **CSV**: Packet tables for spreadsheets
- **PDF**: Professional reports (upcoming)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Streamlit Web UI                        │
│         (File Upload, AI Chat, Packet Viewer)           │
└────────────────┬────────────────────────────────────────┘
                 │
         ┌───────┴────────┐
         │                │
         ▼                ▼
┌─────────────────┐  ┌──────────────────┐
│  Parser Layer   │  │   AI Layer       │
│  - PCAP (Scapy) │  │  Multi-Agent     │
│  - CSV (Pandas) │  │  Load Balancer   │
│  - TXT (Regex)  │  │  Chunking Engine │
└─────────────────┘  └────────┬─────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
      ┌───────────────────┐    ┌──────────────────┐
      │  Cloud Providers  │    │  Local LLM       │
      │  - Groq           │    │  - Ollama        │
      │  - OpenAI         │    │  (100% Offline)  │
      │  - Anthropic      │    └──────────────────┘
      │  - Google Gemini  │
      │  - xAI (Grok)     │
      └───────────────────┘
```

**Design Principles**:

- ✅ **Separation of Concerns**: Parsers are deterministic, AI only receives summaries
- ✅ **Provider Agnostic**: Easy to add new AI backends
- ✅ **Security First**: No raw packet data sent to AI, secrets in `.env`
- ✅ **Offline-First**: Full functionality without internet (Ollama mode)

---

## 📚 Documentation

### Getting Started

- [Setup Guide](docs/SETUP.md) - Detailed installation instructions
- [Quick Reference](docs/QUICK_REFERENCE.md) - Common commands and workflows
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions

### Advanced Topics

- [Weighted Load Balancing](docs/WEIGHTED_BALANCING_GUIDE.md) - Configure AI provider distribution
- [Docker Deployment](docs/DOCKER.md) - Container orchestration
- [UI Development](docs/UI_DEVELOPMENT_WORKFLOW.md) - Frontend customization

### For Contributors

- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [Development Workflow](docs/UI_DEVELOPMENT_WORKFLOW.md) - Code standards
- [Roadmap](docs/ROADMAP.md) - Upcoming features

---

## 🛡️ Security

### Data Privacy

- **Offline Mode**: Ollama processes everything locally, no external connections
- **Cloud Mode**: Only packet **summaries** sent to AI (never raw payloads)
- **Secrets Management**: API keys stored in `.env` (never committed)
- **Input Validation**: File size limits, extension whitelist, rate limiting

### Responsible Disclosure

Found a security issue? Please report privately via:

- **GitHub Security Advisories** (preferred)
- **Email**: See [SECURITY.md](SECURITY.md)

**Do not** create public issues for security vulnerabilities.

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feat/amazing-feature`)
3. **Commit** your changes (`git commit -m 'feat: Add amazing feature'`)
4. **Push** to the branch (`git push origin feat/amazing-feature`)
5. **Open** a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Development Setup

```bash
git clone https://github.com/mfscpayload-690/Sniff-Recon.git
cd Sniff-Recon

# Quick setup (Arch Linux with Ollama)
./dev-setup.sh

# Manual setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.runOnSave true
```

---

## 📊 Project Status

### Current Version: **v1.2.0** (Latest - Ollama Integration)

**Recent Updates** (February 2026):

- ✅ Ollama local LLM support (offline mode)
- ✅ Enhanced provider selection UI with visual badges
- ✅ Explicit provider routing
- ✅ Simplified `.env` configuration
- ✅ Automated development setup script

See [RELEASE_NOTES](docs/RELEASE_NOTES_v1.1.0.md) for full changelog.

### Roadmap Highlights

- 🚧 **Planned**: Real-time packet capture (interface sniffing)
- 🚧 **Planned**: Multi-user authentication
- 🚧 **Planned**: Custom detection rule engine
- 🚧 **Planned**: Threat intel integration (VirusTotal, AlienVault)

See [ROADMAP.md](docs/ROADMAP.md) for complete feature pipeline.

---

## 🏆 Acknowledgments

### Built With

- [Streamlit](https://streamlit.io/) - Web UI framework
- [Scapy](https://scapy.net/) - Packet manipulation
- [PyShark](https://github.com/KimiNewt/pyshark) - PCAP analysis
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [Groq](https://groq.com/) - Fast AI inference
- [OpenAI](https://openai.com/) - GPT models
- [Anthropic](https://anthropic.com/) - Claude models
- [Google Gemini](https://ai.google.dev/) - Gemini API
- [xAI](https://x.ai/) - Grok API

### Contributors

Thanks to all contributors who have helped improve Sniff-Recon!

<a href="https://github.com/mfscpayload-690/Sniff-Recon/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=mfscpayload-690/Sniff-Recon" />
</a>

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 💬 Support & Community

- **Issues**: [GitHub Issues](https://github.com/mfscpayload-690/Sniff-Recon/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mfscpayload-690/Sniff-Recon/discussions)
- **Sponsor**: [Buy Me a Coffee](https://buymeacoffee.com/mfscpayload690)

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by [mfscpayload-690](https://github.com/mfscpayload-690)

</div>
