# 🔍 Sniff Recon - Advanced Network Packet Analyzer

A modern, browser-based network packet analyzer with beautiful UI design and **AI-powered natural language querying**, similar to Wireshark but with enhanced visual appeal and intelligent analysis capabilities.

## ✨ Features

### 🎨 Modern UI Design
- **Beautiful Gradient Backgrounds**: Dark theme with cyan accents
- **Animated Protocol Cards**: Each protocol layer displayed in individual bordered cards
- **Hover Effects**: Interactive elements with smooth animations
- **Responsive Layout**: Works perfectly on all screen sizes
- **Custom Scrollbars**: Styled scrollbars matching the theme

### 🤖 AI-Powered Analysis
- **Natural Language Queries**: Ask questions in plain English about your network traffic
- **Intelligent Insights**: AI analyzes packet data and provides security-focused insights
- **Suspicious Pattern Detection**: Automatic identification of potential threats
- **Interactive AI Interface**: Both GUI and CLI options for AI queries
- **Batch Analysis**: Process multiple queries at once

### 📊 Packet Analysis
- **Interactive Packet Table**: Sortable, filterable packet summary
- **Protocol Layer Dissection**: Detailed breakdown of Ethernet, IP, TCP/UDP, and Application layers
- **Hex Dump Viewer**: Raw packet data in readable hex format
- **Real-time Analysis**: Instant packet inspection on selection

### 📁 File Support
- **PCAP/PCAPNG**: Full packet capture file support
- **CSV**: Network log data in CSV format
- **TXT**: Plain text network logs
- **Large File Support**: Up to 200MB file size limit

### 🔧 Technical Features
- **Streamlit-based**: Modern web framework for rapid development
- **Scapy Integration**: Professional-grade packet parsing
- **AgGrid Tables**: Enterprise-level data grid with advanced features
- **JSON Export**: Download analysis results in JSON format
- **Hugging Face AI**: Powered by Mistral-7B-Instruct-v0.2 model

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Sniff-Recon
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up AI features** (optional but recommended):
   ```bash
   # Create .env file
   echo "HUGGINGFACE_API_KEY=your_api_key_here" > .env
   ```
   
   Get your free API key from: [Hugging Face](https://huggingface.co/settings/tokens)

4. **Run the application**:
   ```bash
   streamlit run sniff_recon_gui.py
   ```

### Usage

1. **Upload a file**: Drag and drop or browse for a packet capture file
2. **View packet table**: Interactive table showing all packets
3. **Select a packet**: Click on any row to analyze that packet
4. **Explore layers**: Each protocol layer is displayed in beautiful cards
5. **Ask AI questions**: Use the AI tab to ask natural language questions
6. **Download results**: Export analysis as JSON

## 🤖 AI Features

### Natural Language Queries
Ask questions like:
- "What are the top 5 source IP addresses?"
- "Are there any suspicious patterns in this traffic?"
- "What protocols are being used most frequently?"
- "Show me the most common destination ports"
- "Is there any evidence of port scanning?"
- "Summarize the overall network activity"
- "Are there any potential security threats?"

### CLI AI Interface
```bash
# Interactive mode
python cli_ai.py -f capture.pcap -i

# Batch mode with specific queries
python cli_ai.py -f capture.pcap -q "What are the top 5 IPs?" "Are there suspicious patterns?"

# Save results to file
python cli_ai.py -f capture.pcap -q "Analyze traffic" -o results.json

# Show packet summary only
python cli_ai.py -f capture.pcap --summary
```

## 🎯 UI Improvements Made

### Visual Enhancements
- **Modern CSS Framework**: Custom styling with Inter font family
- **Gradient Backgrounds**: Beautiful dark theme with cyan accents
- **Card-based Layout**: Each protocol section in individual bordered cards
- **Hover Animations**: Smooth transitions and hover effects
- **Responsive Design**: Mobile-friendly layout

### User Experience
- **Intuitive Navigation**: Clear visual hierarchy with tabs
- **Interactive Elements**: Hover effects and animations
- **Error Handling**: Beautiful error and success messages
- **Loading States**: Smooth transitions between states
- **AI Integration**: Seamless natural language querying

### Technical Improvements
- **Modular Code**: Clean separation of concerns
- **Performance**: Optimized rendering and animations
- **Accessibility**: Proper contrast and readable fonts
- **Cross-browser**: Compatible with modern browsers
- **Security**: Secure API key handling

## 📁 Project Structure

```
Sniff-Recon/
├── main.py                 # Main application entry point
├── sniff_recon_gui.py      # Streamlit GUI application
├── display_packet_table.py # Modern packet table display
├── ui_packet_viewer.py     # Enhanced packet viewer
├── ai_module.py           # AI query engine
├── ai_query_interface.py  # Streamlit AI interface
├── cli_ai.py             # CLI AI interface
├── setup_api_key.py       # API key setup utility
├── test_hf_api.py         # Hugging Face API testing utility
├── parsers/               # File parsing modules
│   ├── pcap_parser.py     # PCAP file parser
│   ├── csv_parser.py      # CSV file parser
│   └── txt_parser.py      # TXT file parser
├── utils/                  # Utility functions
│   └── helpers.py          # Helper functions
├── output/                 # Generated output files
│   └── summary.json        # Analysis summary file
├── requirements.txt        # Python dependencies
├── SETUP.md               # AI setup guide
├── TROUBLESHOOTING.md     # Troubleshooting guide
├── LICENSE                # License file
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## 🎨 Design System

### Color Palette
- **Primary**: `#00ffff` (Cyan)
- **Secondary**: `#00b3b3` (Dark Cyan)
- **Background**: `#0f0f23` to `#16213e` (Gradient)
- **Text**: `#e0e0e0` (Light Gray)
- **Cards**: `rgba(30, 30, 30, 0.9)` (Semi-transparent Dark)

### Typography
- **Font Family**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700
- **Monospace**: Courier New for technical data

### Animations
- **Fade In**: Cards appear with staggered animation
- **Hover Effects**: Cards lift and glow on hover
- **Smooth Transitions**: 0.3s cubic-bezier transitions

## 🔮 Future Enhancements

### Planned Features
- **Advanced AI Models**: Support for multiple AI models
- **Real-time Capture**: Live packet monitoring with AI analysis
- **Advanced Filtering**: Complex packet filtering with AI assistance
- **Export Options**: PDF, HTML, and CSV reports with AI insights
- **Plugin System**: Extensible architecture for custom analyzers

### UI Improvements
- **Dark/Light Theme**: User-selectable themes
- **Customizable Layout**: Drag-and-drop interface
- **Advanced Visualizations**: Packet flow diagrams with AI annotations
- **Keyboard Shortcuts**: Power user features

## 🔐 Security & Privacy

- **API Key Security**: Keys stored in environment variables, never hardcoded
- **Local Processing**: Packet analysis happens locally
- **Secure Communication**: HTTPS for AI API calls
- **No Data Storage**: AI queries are not stored permanently

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Streamlit**: For the amazing web framework
- **Scapy**: For professional packet manipulation
- **AgGrid**: For the powerful data grid component
- **Hugging Face**: For the AI inference API
- **Inter Font**: For the beautiful typography

---

**Made with ❤️ for network analysis enthusiasts**
