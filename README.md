# 🔍 Sniff Recon - Advanced Network Packet Analyzer

A modern, browser-based network packet analyzer with beautiful UI design, similar to Wireshark but with enhanced visual appeal and user experience.

## ✨ Features

### 🎨 Modern UI Design
- **Beautiful Gradient Backgrounds**: Dark theme with cyan accents
- **Animated Protocol Cards**: Each protocol layer displayed in individual bordered cards
- **Hover Effects**: Interactive elements with smooth animations
- **Responsive Layout**: Works perfectly on all screen sizes
- **Custom Scrollbars**: Styled scrollbars matching the theme

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

3. **Run the application**:
   ```bash
   streamlit run sniff_recon_gui.py
   ```

### Usage

1. **Upload a file**: Drag and drop or browse for a packet capture file
2. **View packet table**: Interactive table showing all packets
3. **Select a packet**: Click on any row to analyze that packet
4. **Explore layers**: Each protocol layer is displayed in beautiful cards
5. **Download results**: Export analysis as JSON

## 🎯 UI Improvements Made

### Visual Enhancements
- **Modern CSS Framework**: Custom styling with Inter font family
- **Gradient Backgrounds**: Beautiful dark theme with cyan accents
- **Card-based Layout**: Each protocol section in individual bordered cards
- **Hover Animations**: Smooth transitions and hover effects
- **Responsive Design**: Mobile-friendly layout

### User Experience
- **Intuitive Navigation**: Clear visual hierarchy
- **Interactive Elements**: Hover effects and animations
- **Error Handling**: Beautiful error and success messages
- **Loading States**: Smooth transitions between states

### Technical Improvements
- **Modular Code**: Clean separation of concerns
- **Performance**: Optimized rendering and animations
- **Accessibility**: Proper contrast and readable fonts
- **Cross-browser**: Compatible with modern browsers

## 📁 Project Structure

```
Sniff-Recon/
├── sniff_recon_gui.py      # Main application entry point
├── display_packet_table.py # Modern packet table display
├── ui_packet_viewer.py     # Enhanced packet viewer
├── parsers/                # File parsing modules
│   ├── pcap_parser.py     # PCAP file parser
│   ├── csv_parser.py      # CSV file parser
│   └── txt_parser.py      # TXT file parser
├── utils/                  # Utility functions
├── output/                 # Generated output files
└── requirements.txt        # Python dependencies
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
- **AI Integration**: Natural language packet analysis
- **Advanced Filtering**: Complex packet filtering
- **Export Options**: PDF, HTML, and CSV reports
- **Plugin System**: Extensible architecture

### UI Improvements
- **Dark/Light Theme**: User-selectable themes
- **Customizable Layout**: Drag-and-drop interface
- **Advanced Visualizations**: Packet flow diagrams
- **Keyboard Shortcuts**: Power user features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
---

**Made with ❤️ for network analysis enthusiasts**
