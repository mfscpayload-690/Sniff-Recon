# Sniff Recon 🔍

**Multi-Agent AI-Powered PCAP Analysis Tool**

Sniff Recon is a Python CLI/GUI application that analyzes PCAP (Packet Capture) logs using multiple AI providers for intelligent, scalable network traffic analysis and security insights.

## Features ✨

- 🤖 **Multi-Agent AI System**: Support for Groq, OpenAI, Anthropic Claude, and more
- ⚖️ **Load Balancing**: Automatic distribution across multiple AI providers
- 📊 **Large File Support**: Intelligent chunking for files >50MB with 70k+ packets
- 🔐 **Secure Configuration**: Environment-based API key management
- 🛡️ **Advanced Error Handling**: Comprehensive error handling with fallback analysis
- ⚡ **Async Processing**: Concurrent analysis for faster results
- 🎯 **Smart Triage**: Pre-filtering suspicious packets for focused AI analysis
- 🔄 **Retry Logic**: Automatic retry with exponential backoff

## Quick Start 🚀

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd Sniff-Recon

# Install dependencies
pip install -r requirements.txt
```

### 2. Multi-Agent AI Setup (Recommended)

For enhanced performance and reliability, set up multiple AI providers:

```bash
# Run the interactive setup script
python setup_multi_agent.py
```

This will guide you through configuring:
- **Groq** (Fast, free tier available)
- **OpenAI** (High quality, paid)
- **Anthropic Claude** (Excellent for analysis)

Or manually create a `.env` file:

```env
# Multiple AI Providers
GROQ_API_KEY=gsk_your_groq_key_here
GROQ_MODEL=llama3-8b-8192

OPENAI_API_KEY=sk_your_openai_key_here
OPENAI_MODEL=gpt-3.5-turbo

ANTHROPIC_API_KEY=sk-ant_your_anthropic_key_here
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# System Configuration
CHUNK_SIZE_MB=5
MAX_PACKETS_PER_CHUNK=5000
```

### 3. Run the Enhanced App

```bash
# Enhanced CLI with multi-agent support
python enhanced_cli_ai.py -f <your-pcap-file.pcap> -i

# Original CLI (single provider)
python cli_ai.py -f <your-pcap-file.pcapng> -i
```

## Usage 💡

### Basic Usage

1. **Interactive Mode**: 
   ```bash
   python enhanced_cli_ai.py -f capture.pcap -i
   ```

2. **Single Query**: 
   ```bash
   python enhanced_cli_ai.py -f capture.pcap -q "Show me security threats"
   ```

3. **Batch Analysis**: 
   ```bash
   python enhanced_cli_ai.py -f capture.pcap -b queries.txt
   ```

### Large File Handling 📊

The system automatically handles large files (>50MB, >70k packets) by:

- **Smart Chunking**: Splits data into 5MB/5000 packet chunks
- **Concurrent Processing**: Analyzes chunks in parallel
- **Intelligent Triage**: Pre-filters suspicious packets for focused analysis
- **Memory Optimization**: Streams packets to avoid memory issues

```bash
# Configure chunking parameters
python enhanced_cli_ai.py -f large_capture.pcap -i --chunk-size 10 --max-packets 10000
```

### Example Queries

```
> "Analyze this network traffic for security threats and anomalies"
> "What are the most active IP addresses and what might they be doing?"
> "Identify any suspicious port usage or protocol patterns"
> "Look for signs of network scanning or reconnaissance"
> "Analyze the traffic for potential data exfiltration attempts"
> "What protocols are being used and are they appropriate?"
```

### Advanced Features

- **Multi-Provider Fallback**: If one AI provider fails, others continue
- **Response Combining**: Merges analysis from multiple chunks
- **Performance Metrics**: Shows processing time and token usage
- **Progress Tracking**: Real-time progress bars for large files

## Error Handling 🛠️

The app handles various error scenarios:

- **401 Unauthorized**: Invalid API key
- **429 Rate Limited**: Too many requests (automatic retry with backoff)
- **404 Not Found**: Invalid model name
- **Network Timeouts**: Connection issues
- **Missing Environment Variables**: Configuration problems

## Future Features 🎯

### Planned PCAP Analysis Features

1. **PCAP File Processing**
   - Load and parse PCAP files using scapy or pyshark
   - Extract packet metadata (timestamps, protocols, IPs, ports)
   - Generate summary statistics

2. **Natural Language PCAP Queries**
   - "Show me all HTTP requests to suspicious domains"
   - "Find packets with unusual port activity"
   - "Analyze traffic patterns between 10:00 AM and 2:00 PM"
   - "Identify potential security threats in this capture"

3. **AI-Powered Analysis**
   - Automatic threat detection and classification
   - Anomaly detection in network traffic
   - Behavioral analysis of network flows
   - Security incident correlation

4. **Advanced Features**
   - Real-time packet capture analysis
   - Network topology mapping
   - Protocol-specific analysis (HTTP, DNS, TLS, etc.)
   - Export findings to reports (PDF, JSON, CSV)
   - Integration with threat intelligence feeds

## Troubleshooting 🔧

### Common Issues

1. **"GROQ_API_KEY not found"**
   - Run `python setup_api_key.py` to configure your key.
   - Check that your `.env` file exists and contains the API key.

2. **"Invalid API key"**
   - Verify your API key is correct and starts with `gsk_`.

3. **"Network connection error"**
   - Check your internet connection.
   - Verify firewall settings aren't blocking requests to the Groq API.

### Getting Help

If you encounter issues:

1. Run `python setup_api_key.py` to set up your key.
2. Verify your `.env` configuration.
3. Test your internet connection.

## Security 🔒

- **API Key Protection**: Never hardcode API keys in your code
- **Environment Variables**: All sensitive data is stored in `.env` files
- **Input Validation**: User inputs are properly sanitized
- **Error Handling**: Sensitive information is not exposed in error messages

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- Groq for providing the free, high-speed API
- The Python community for excellent libraries
- Network security researchers for inspiration

---

**Happy Network Analysis! 🔍📊**
