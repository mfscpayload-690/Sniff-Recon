# 🤖 AI Setup Guide for Sniff Recon

This guide will help you set up the AI-powered packet analysis features in Sniff Recon.

## 🔑 Getting Your Hugging Face API Key

1. **Visit Hugging Face**: Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

2. **Create Account**: Sign up for a free account if you don't have one

3. **Generate API Key**: 
   - Click "New token"
   - Give it a name (e.g., "Sniff Recon AI")
   - Select "Read" permissions
   - Copy the generated token

## 📁 Environment Setup

1. **Create .env file**: In your project root, create a file named `.env`

2. **Add your API key**:
   ```bash
   # .env file
   HUGGINGFACE_API_KEY=your_actual_api_key_here
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Streamlit GUI
```bash
streamlit run sniff_recon_gui.py
```

### CLI Interface
```bash
# Interactive mode
python cli_ai.py -f capture.pcap -i

# Batch mode
python cli_ai.py -f capture.pcap -q "What are the top 5 IPs?" "Are there suspicious patterns?"

# Show suggested queries
python cli_ai.py --suggested
```

## 💡 Example AI Queries

- "What are the top 5 source IP addresses?"
- "Are there any suspicious patterns in this traffic?"
- "What protocols are being used most frequently?"
- "Show me the most common destination ports"
- "Is there any evidence of port scanning?"
- "Summarize the overall network activity"
- "Are there any potential security threats?"

## 🔧 Troubleshooting

### API Key Issues
- Make sure your `.env` file is in the project root
- Verify the API key is correct and has proper permissions
- Check that `python-dotenv` is installed

### Network Issues
- Ensure you have internet connectivity
- The AI model requires an active connection to Hugging Face servers

### File Format Issues
- Currently supports `.pcap` and `.pcapng` files
- Make sure your packet capture files are valid

## 📊 Features

### AI Analysis Capabilities
- **Natural Language Queries**: Ask questions in plain English
- **Protocol Analysis**: Automatic detection of TCP, UDP, ICMP, etc.
- **Suspicious Pattern Detection**: Identifies potential security threats
- **Statistical Analysis**: Provides comprehensive packet statistics
- **Interactive Interface**: Both GUI and CLI options

### Security Features
- **Environment Variable Storage**: API keys stored securely
- **No Hardcoded Credentials**: Follows security best practices
- **Error Handling**: Graceful handling of API failures

## 🎯 Next Steps

1. **Test with Sample Data**: Try the AI features with a small packet capture
2. **Explore Queries**: Experiment with different types of questions
3. **Customize Analysis**: Modify the AI prompts for specific use cases
4. **Integrate with Workflows**: Use the CLI for automated analysis

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your API key and permissions
3. Ensure all dependencies are installed
4. Test with a simple packet capture first 