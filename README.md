# Sniff Recon

**AI-Powered Network Packet Analyzer**

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-GUI-FF4B4B?logo=streamlit&logoColor=white)
![PyShark](https://img.shields.io/badge/PyShark-Packet%20Analysis-00A4EF?logo=wireshark&logoColor=white)
![tshark](https://img.shields.io/badge/tshark-Network%20Analysis-1679A7?logo=wireshark&logoColor=white)

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-yellow?logo=buymeacoffee)](https://buymeacoffee.com/mfscpayload690)

Sniff Recon is a modern, multi-agent network packet analyzer with a beautiful Streamlit GUI. It supports PCAP, CSV, and TXT files, and provides natural language AI analysis using Groq, OpenAI, Google Gemini, xAI (Grok), and Anthropic.

## Features

- Modern Streamlit web interface (cyberpunk dark theme)
- Upload and analyze PCAP, PCAPNG, CSV, or TXT files
- Multi-agent AI: Groq, OpenAI, Google Gemini, xAI (Grok), Anthropic
- Natural language querying for network security insights
- Automatic suspicious packet detection and clustering
- Interactive packet tables (AgGrid)
- Layer-by-layer protocol inspection (Ethernet, IP, TCP/UDP, Application)
- Export results as JSON
- Handles large files (up to 200MB) with chunking
- Dockerized for easy deployment

## Quick Start

### 🌐 Live Web App (Easiest)

**Try it instantly - no installation required:**

👉 **[https://sniff-recon.up.railway.app](https://sniff-recon.up.railway.app)**

Simply upload your PCAP, CSV, or TXT file and start analyzing! The web app is fully functional with AI-powered analysis.

---

### 🐳 Docker (Self-Hosted)

```bash
git clone https://github.com/mfscpayload-690/Sniff-Recon.git
cd Sniff-Recon

# Add your API keys to .env (see .env.template)
# GROQ_API_KEY=...
# OPENAI_API_KEY=...
# GOOGLE_API_KEY=...
# XAI_API_KEY=...
# ANTHROPIC_API_KEY=...

docker-compose up -d
# Or: .\docker-start.ps1 (Windows)

# Access at http://localhost:8501
```

**Container Management:**

```bash
docker logs sniff-recon-app -f      # View logs
docker-compose down                 # Stop the container
docker-compose restart              # Restart the container
docker-compose up -d --build        # Rebuild after code changes
```

---

### 💻 Local Development

```bash
git clone https://github.com/mfscpayload-690/Sniff-Recon.git
cd Sniff-Recon

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# or: source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the app
python start_gui.py
# Or: streamlit run app.py

# Access at http://localhost:8501
```

## Usage

1. Upload a packet capture (PCAP/CSV/TXT)
2. View protocol stats, top IPs, suspicious patterns
3. Inspect packets layer-by-layer
4. Ask questions in natural language ("Show suspicious packets", "Analyze traffic patterns")
5. Export results as JSON

## AI Providers

- **Groq**: Fast, free tier available
- **OpenAI**: High quality, paid
- **Google Gemini**: Large context window, free tier
- **xAI (Grok)**: Real-time knowledge, 128K context window (requires credits)
- **Anthropic**: Premium quality (Claude)

Providers are auto-detected from `.env`. Load balancing and failover are automatic.

## Architecture

```
Streamlit GUI → Parser Layer → Multi-Agent AI → Scapy Packet Analysis
```

## Troubleshooting

- Install dependencies: `pip install -r requirements.txt`
- File upload fails: Check file size (<200MB) and format
- AI not working: Verify API keys in `.env`
- Docker issues: `docker-compose logs -f`

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more.

## Project Structure

```
Sniff-Recon/
├── sniff_recon_gui.py          # Main Streamlit app
├── src/ai/multi_agent_ai.py    # Multi-provider AI system
├── src/ai/ai_module.py         # Fallback AI + packet filtering
├── src/ui/display_packet_table.py # AgGrid tables
├── src/ai/ai_query_interface.py   # AI chat interface
├── parsers/                    # Format-specific parsers
├── utils/                      # Helper functions
├── Dockerfile                  # Container image
├── docker-compose.yml          # Orchestration
├── requirements.txt            # Python dependencies
```

## Security

- API keys in `.env` (never commit secrets)
- File size and format validation
- Error handling: no sensitive info in logs

## Developers

| Name           | Role                        | GitHub                                      |
|----------------|-----------------------------|----------------------------------------------|
| Aravind Lal    | Lead Developer, Backend/AI  | [@mfscpayload-690](https://github.com/mfscpayload-690) |
| Devu Krishna   | UI/UX Developer, Frontend   | [@krizzdev7](https://github.com/krizzdev7)   |

## License

MIT License. See [LICENSE](LICENSE).

---

Made with ❤️ by the Sniff Recon Team

## Support the Project

If you find Sniff Recon useful, you can support ongoing development:

- Set BUYMEACOFFEE_URL in your `.env` to display a donation button in the app sidebar.
- Replace the badge link at the top of this README with your actual Buy Me a Coffee URL.

Thank you for your support!
