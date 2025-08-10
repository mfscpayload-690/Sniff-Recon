# 🔍 Sniff Recon v1.0.0 - "GUI Launch"

## 🚀 Initial Release: AI-Powered Network Packet Analyzer

### ✨ Features

- **🖥️ Modern Web GUI**: Beautiful Streamlit-based interface with cyberpunk dark theme
- **📁 Multi-Format Support**: Analyze `.pcap`, `.pcapng`, `.csv`, and `.txt` files up to 200MB
- **📊 Interactive Packet Tables**: Smooth scrolling and filtering with `streamlit-aggrid`
- **🤖 AI-Powered Analysis**: Optional integration with Groq, OpenAI, and Anthropic for intelligent insights
- **🎯 Drag & Drop Interface**: Effortless file uploads and intuitive navigation
- **💾 Export Capabilities**: Download analysis results as JSON reports

### 🔧 Technical Stack

- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Python with Scapy for packet parsing
- **AI Integration**: Multi-provider support (Groq, OpenAI, Anthropic)
- **Data Processing**: Pandas and NumPy for efficient analysis
- **Visualization**: Matplotlib for charts and graphs

### 🚀 Quick Start

```bash
# Setup virtual environment
python3 -m venv venv_gui
source venv_gui/bin/activate
pip install -r requirements.txt

# Launch GUI
./run_gui.sh
# or
python start_gui.py
```

### 📋 What You Get

- **Packet Analysis Tab**: Comprehensive packet statistics and protocol distribution
- **AI Analysis Tab**: Natural language queries about your network traffic (optional)
- **Export Tab**: Download results and view raw data
- **Real-time Processing**: Live progress tracking for large files

### 🎯 Perfect For

- Security researchers analyzing network traffic
- Network administrators investigating incidents  
- Students learning packet analysis
- Anyone who needs intuitive PCAP file analysis

### 🌐 Access

Access the GUI at `http://localhost:8501` and start analyzing! 🔬

### 📦 Dependencies

See `requirements.txt` for the complete list of dependencies. Key packages include:
- `streamlit>=1.25.0`
- `streamlit-aggrid>=1.0.5`
- `scapy>=2.5.0`
- `pandas>=2.0.0`
- `matplotlib>=3.7.0`

### 🔗 System Requirements

- Python 3.8+
- 4GB+ RAM (for large packet files)
- Internet connection (for AI features)
- Supported OS: Windows, macOS, Linux

---

**Happy Network Analysis! 🔍📊**
