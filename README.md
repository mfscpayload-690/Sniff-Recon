# Sniff Recon 🔍

**AI-Powered Network Packet Analyzer - GUI Edition**

Sniff Recon is a user-friendly GUI application built with Streamlit that analyzes network packet capture files (PCAP, CSV, TXT) with AI-powered insights for network traffic analysis and security monitoring.

## Features ✨

- 🖥️ **Modern Web-Based GUI**: Beautiful, responsive interface built with Streamlit
- 📁 **Multiple File Formats**: Support for .pcap, .pcapng, .csv, and .txt files
- 🤖 **AI-Powered Analysis**: Intelligent packet analysis and threat detection
- 📊 **Interactive Visualizations**: Real-time packet tables and statistics
- 💾 **Export Capabilities**: Download analysis results as JSON
- 🎨 **Beautiful Dark Theme**: Modern cyberpunk-inspired design
- ⚡ **Real-Time Processing**: Live progress tracking for large files
- 🔍 **Detailed Packet Inspection**: Comprehensive packet metadata display

## Quick Start 🚀

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd Sniff-Recon

# Create and activate virtual environment (recommended)
python3 -m venv venv_gui
source venv_gui/bin/activate  # On Windows: venv_gui\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. AI Setup (Optional)

For AI-powered analysis features, create a `.env` file with your API keys:

```env
# AI Providers (Optional - for enhanced analysis)
GROQ_API_KEY=your_groq_key_here
OPENAI_API_KEY=your_openai_key_here
# Add other provider keys as needed
```

### 3. Launch the GUI

```bash
# Option 1: Use the shell script (if in venv)
./run_gui.sh

# Option 2: Use the Python startup script
python start_gui.py

# Option 3: Start directly with Streamlit
streamlit run sniff_recon_gui.py
```

**Note**: If you're using the virtual environment, the shell script `./run_gui.sh` will automatically activate it for you.

The application will open in your default web browser at `http://localhost:8501`

## Usage 💡

### File Upload
1. **Drag & Drop**: Simply drag your packet capture file into the upload area
2. **Browse**: Click the upload button to browse for files
3. **Supported Formats**: .pcap, .pcapng, .csv, .txt (up to 200MB)

### Analysis Tabs

#### 📊 Packet Analysis
- View comprehensive packet statistics
- Interactive packet table with filtering
- Protocol distribution charts
- Source/destination IP analysis

#### 🤖 AI Analysis (If configured)
- Quick AI-powered threat assessment
- Natural language query interface
- Ask questions about your network traffic
- Get intelligent insights and recommendations

#### 💾 Export Results
- Download analysis results as JSON
- View raw data in formatted display
- Save reports for further analysis

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

1. **"Module not found" errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check that you're in the correct directory

2. **File upload failures**
   - Ensure your file is under 200MB
   - Check file format is supported (.pcap, .pcapng, .csv, .txt)
   - Verify file permissions

3. **GUI not loading**
   - Make sure Streamlit is installed: `pip install streamlit`
   - Try running: `streamlit run sniff_recon_gui.py --server.port 8501`
   - Check if port 8501 is available

4. **AI Analysis not working**
   - Verify your `.env` file contains valid API keys
   - Check your internet connection
   - Ensure API keys are properly formatted

### Getting Help

If you encounter issues:

1. Check that all dependencies are installed correctly
2. Verify your `.env` file configuration (if using AI features)
3. Ensure your network connection is stable
4. Try with a smaller test file first

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

---

**Happy Network Analysis! 🔍📊**
