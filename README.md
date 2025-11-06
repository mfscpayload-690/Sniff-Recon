# Sniff Recon 🔍

**AI-Powered Network Packet Analyzer with Modern GUI**

Sniff Recon is a powerful network packet analyzer built with Streamlit that provides AI-powered insights for network traffic analysis and security monitoring. Analyze PCAP, CSV, and TXT packet captures with natural language queries and intelligent threat detection.

## Features ✨

- 🖥️ **Modern Web-Based GUI**: Beautiful, responsive Streamlit interface
- 📁 **Multiple File Formats**: Support for PCAP, PCAPNG, CSV, and TXT files
- 🤖 **Multi-Agent AI System**: Leverages Groq, OpenAI, and Anthropic for intelligent analysis
- 🔍 **Smart Packet Filtering**: Automatic suspicious packet detection and clustering
- 📊 **Interactive Visualizations**: Real-time packet tables with AgGrid
- 💾 **Export Capabilities**: Download analysis results as JSON
- 🎨 **Cyberpunk Dark Theme**: Modern UI with custom CSS styling
- ⚡ **Large File Support**: Handles files up to 200MB with chunking
- � **Detailed Packet Inspection**: Layer-by-layer protocol analysis (Ethernet, IP, TCP/UDP, Application)
- 🐳 **Docker Support**: Containerized deployment with health checks

## Quick Start 🚀

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/mfscpayload-690/Sniff-Recon.git
cd Sniff-Recon

# Create .env file with your AI API keys (optional)
# GROQ_API_KEY=your_key_here
# OPENAI_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here

# Build and run with Docker Compose
docker-compose up -d

# Access at http://localhost:8501
```

### Option 2: Local Installation

```bash
# Clone the repository
git clone https://github.com/mfscpayload-690/Sniff-Recon.git
cd Sniff-Recon

# Create and activate virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch the GUI
python start_gui.py
```

The application will open in your browser at `http://localhost:8501`

## Usage 💡

### Analyzing Packet Captures

1. **Upload File**: Drag and drop or browse for your packet capture file (PCAP, PCAPNG, CSV, TXT)
2. **View Statistics**: See protocol distribution, top talkers, and packet summaries
3. **Inspect Packets**: Click on any packet for detailed layer-by-layer analysis
4. **AI Analysis**: Use natural language queries like:
   - "Show me all suspicious packets"
   - "Find potential security threats"
   - "Analyze traffic patterns"
   - "What ports are being scanned?"
5. **Export Results**: Download comprehensive analysis as JSON

### AI-Powered Features

The app works **with or without AI**:
- ✅ **With AI**: Get intelligent threat detection, natural language querying, and automated analysis
- ✅ **Without AI**: Still get full packet parsing, statistics, and manual inspection capabilities

AI providers are automatically detected from your `.env` file. The system uses a multi-agent approach with load balancing across available providers.

## Architecture 🏗️

```
┌─────────────────────────────────────────────────────────┐
│                  Streamlit GUI Layer                    │
│  (sniff_recon_gui.py, display_packet_table.py,         │
│   ai_query_interface.py)                                │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                   Parser Layer                          │
│  (pcap_parser.py, csv_parser.py, txt_parser.py)        │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              AI Multi-Agent System                      │
│  • Groq Provider (llama-3.3-70b-versatile)             │
│  • OpenAI Provider (gpt-4o)                            │
│  • Anthropic Provider (claude-3-5-sonnet-20241022)     │
│  • Load balancing & automatic chunking                 │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│           Scapy Packet Analysis Engine                  │
│  • Layer-by-layer parsing (Ethernet → IP → TCP/UDP)    │
│  • Suspicious packet filtering                         │
│  • IP clustering and summarization                     │
└─────────────────────────────────────────────────────────┘
```

### Key Components

- **Parsers**: Convert PCAP/CSV/TXT → Pandas DataFrames
- **Multi-Agent AI**: Parallel processing across multiple LLM providers with 5MB/5000-packet chunking
- **Packet Filtering**: 3-stage process (filter suspicious → cluster by IP → summarize) reduces payload by ~90%
- **Session State**: Streamlit state management for AI query history and user preferences

## Troubleshooting 🔧

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

### Common Issues

- **Module not found**: Run `pip install -r requirements.txt`
- **File upload failures**: Check file size (<200MB) and format (PCAP/CSV/TXT)
- **AI not working**: Verify `.env` file contains valid API keys
- **Docker issues**: Check logs with `docker-compose logs -f`

For more help, check the [SETUP.md](SETUP.md) guide.

## Technology Stack �️

- **Frontend**: Streamlit, st-aggrid, custom CSS
- **Packet Analysis**: Scapy, PyShark
- **AI/ML**: Multi-agent system (Groq, OpenAI, Anthropic)
- **Data Processing**: Pandas, asyncio/aiohttp
- **Deployment**: Docker, Docker Compose
- **Languages**: Python 3.11+

## Development 👨‍💻

### Project Structure

```
Sniff-Recon/
├── sniff_recon_gui.py          # Main Streamlit app
├── multi_agent_ai.py           # Multi-provider AI system
├── ai_module.py                # Fallback AI + packet filtering
├── display_packet_table.py     # AgGrid packet tables
├── ai_query_interface.py       # AI chat interface
├── parsers/                    # Format-specific parsers
│   ├── pcap_parser.py
│   ├── csv_parser.py
│   └── txt_parser.py
├── utils/                      # Helper functions
│   └── helpers.py
├── .github/
│   └── copilot-instructions.md # AI development guidelines
├── Dockerfile                  # Container image definition
├── docker-compose.yml          # Multi-container orchestration
└── requirements.txt            # Python dependencies
```

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-cov

# Run tests (when implemented)
pytest tests/ -v

# Run with coverage
pytest --cov=. --cov-report=html
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes following the code style in `.github/copilot-instructions.md`
4. Test thoroughly with sample PCAP files
5. Submit a pull request to `main` branch

**Branch Workflow**:
- `main`: Production-ready code
- `front-end-test`: UI/UX development (maintained by [@krizzdev7](https://github.com/krizzdev7))
- Feature branches: Temporary branches for specific features

## Security 🔒

- **API Key Protection**: Store API keys in `.env` (gitignored)
- **Input Validation**: File size limits and format validation
- **Error Handling**: Sensitive information never exposed in logs
- **Docker Security**: Regular `apt-get upgrade` for vulnerability patching
- **No Hardcoded Secrets**: All credentials via environment variables

## Developers 👥

| Developer | Role | GitHub |
|-----------|------|--------|
| **Aravind Lal** | Lead Developer, Backend & AI Architecture | [@mfscpayload-690](https://github.com/mfscpayload-690) |
| **Devu Krishna** | UI/UX Developer, Frontend Design | [@krizzdev7](https://github.com/krizzdev7) |

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Built with [Streamlit](https://streamlit.io/) for the web interface
- Powered by [Scapy](https://scapy.net/) for packet analysis
- AI capabilities via [Groq](https://groq.com/), [OpenAI](https://openai.com/), and [Anthropic](https://anthropic.com/)

---

**Happy Network Analysis! 🔍📊**

Made with ❤️ by the Sniff Recon Team
