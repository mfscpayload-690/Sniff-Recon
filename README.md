# Sniff Recon 🔍

**AI-Powered PCAP Analysis Tool**

Sniff Recon is a Python CLI/GUI application that analyzes PCAP (Packet Capture) logs using the Groq API for intelligent, real-time network traffic analysis and security insights.

## Features ✨

- 🤖 **Groq API Integration**: Blazing-fast natural language queries for PCAP analysis.
- 🔐 **Secure Configuration**: Environment-based API key management
- 🛡️ **Error Handling**: Comprehensive error handling for API issues
- 🔄 **Retry Logic**: Automatic retry with exponential backoff
- 📊 **Future-Ready**: Framework for advanced PCAP analysis features

## Quick Start 🚀

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd Sniff-Recon

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

The app uses the Groq API for its AI analysis. Follow the `SETUP.md` guide to get your free API key and configure the application.

```env
# Sniff Recon - Groq API Configuration
GROQ_API_KEY=gsk_your_actual_api_key_here
MODEL_NAME=llama3-8b-8192
```

### 3. Run the App

```bash
python cli_ai.py -f <your-pcap-file.pcapng> -i
```

## Usage 💡

### Basic Usage

1. **Start the app**: Run `python cli_ai.py -f <your-pcap-file.pcapng> -i`
2. **Ask questions**: Enter natural language queries about your network traffic.

### Example Queries

```
> "Hello! How can you help me analyze network traffic?"
> "What should I look for when analyzing suspicious network activity?"
> "Explain the difference between TCP and UDP protocols"
> "How can I identify potential security threats in a PCAP file?"
```

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
