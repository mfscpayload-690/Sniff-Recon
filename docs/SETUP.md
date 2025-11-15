# 🤖 AI Setup Guide for Sniff Recon GUI

This guide will help you set up the AI-powered packet analysis features in Sniff Recon's GUI interface.

## 🔑 Getting AI API Keys (Optional)

### Groq API (Free Tier Available)
1. **Visit Groq**: Go to [https://console.groq.com/keys](https://console.groq.com/keys)
2. **Create Account**: Sign up for a free account if you don't have one.
3. **Generate API Key**:
   - Click "Create API Key"
   - Give it a name (e.g., "Sniff Recon AI")
   - Copy the generated key.

### OpenAI API (Paid)
1. **Visit OpenAI**: Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. **Create Account**: Sign up and add payment method
3. **Generate API Key**: Create a new secret key

## 📁 Environment Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create .env File** (for AI features):
   ```env
   # Optional AI Providers
   GROQ_API_KEY=your_groq_key_here
   OPENAI_API_KEY=your_openai_key_here
   ```

## 🚀 Usage

### Launch the GUI
```bash
# Using the launcher script (recommended)
python scripts/start_gui.py

# Or run directly with Streamlit
streamlit run app.py
```

The application will open at `http://localhost:8501` in your web browser.

## 💡 Example AI Queries

- "What are the top 5 source IP addresses?"
- "Are there any suspicious patterns in this traffic?"
- "What protocols are being used most frequently?"
- "Show me the most common destination ports"
- "Is there any evidence of port scanning?"
- "Summarize the overall network activity"
- "Are there any potential security threats?"

## 🔧 Troubleshooting

### GUI Loading Issues
- Ensure Streamlit is installed: `pip install streamlit`
- Check if port 8501 is available
- Try running with a specific port: `streamlit run app.py --server.port 8502`

### File Upload Issues
- Supports `.pcap`, `.pcapng`, `.csv`, and `.txt` files
- File size limit is 200MB
- Make sure your packet capture files are valid

### AI Analysis Issues
- Verify your `.env` file contains valid API keys
- Check your internet connection
- AI features are optional - the app works without them

## 📊 Features

### AI Analysis Capabilities
- **Natural Language Queries**: Ask questions in plain English through the GUI
- **Protocol Analysis**: Automatic detection of TCP, UDP, ICMP, etc.
- **Suspicious Pattern Detection**: Identifies potential security threats
- **Statistical Analysis**: Provides comprehensive packet statistics
- **Web-Based Interface**: Modern, responsive GUI built with Streamlit
- **Interactive Visualizations**: Real-time charts and tables

### Security Features
- **Environment Variable Storage**: API keys stored securely
- **No Hardcoded Credentials**: Follows security best practices
- **Error Handling**: Graceful handling of API failures
- **File Validation**: Secure file upload and processing

## 🎯 Next Steps

1. **Test with Sample Data**: Upload a small packet capture file to test
2. **Explore the GUI**: Navigate through different analysis tabs
3. **Try AI Features**: Ask questions about your network traffic (if API keys configured)
4. **Export Results**: Download analysis results as JSON files

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section in README.md
2. Ensure all dependencies are installed correctly
3. Verify your .env file configuration (if using AI features)
