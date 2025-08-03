# 🛠️ Troubleshooting Guide

This guide helps resolve common issues with Sniff Recon.

## 🔑 API Key and Configuration Issues

**1. "GROQ_API_KEY not found in environment variables"**

- **Cause**: The application cannot find your Groq API key.
- **Solution**:
  1. Run the setup script: `python setup_api_key.py`
  2. Enter your API key when prompted.
  3. This will create a `.env` file in the project root with your key.

**2. "Invalid API key"**

- **Cause**: The API key is incorrect or has been revoked.
- **Solution**:
  1. Get a new key from [https://console.groq.com/keys](https://console.groq.com/keys).
  2. Run `python setup_api_key.py` to update your key.
  3. Make sure the key starts with `gsk_`.

**3. "Failed to parse .env file"**

- **Cause**: The `.env` file is formatted incorrectly.
- **Solution**:
  - Make sure the file contains `GROQ_API_KEY=your_key_here` on a single line.
  - You can delete the `.env` file and run `python setup_api_key.py` again to create a fresh one.

## 🌐 Network and API Connectivity Issues

**1. "API request failed with status 401: Unauthorized"**

- **Cause**: Your API key is invalid.
- **Solution**: Follow the steps for an "Invalid API key" above.

**2. "API request failed with status 429: Rate Limit Exceeded"**

- **Cause**: You have exceeded the free rate limits for the Groq API.
- **Solution**:
  - Wait a few minutes and try again.
  - Check বড়ো's documentation for information on rate limits.

**3. "Request error: Connection timed out"**

- **Cause**: The application cannot connect to the Groq API servers.
- **Solution**:
  - Check your internet connection.
  - Ensure your firewall or proxy is not blocking access to `https://api.groq.com`.

## 📦 Dependency and Module Issues

**1. "ModuleNotFoundError: No module named 'scapy'" (or other modules)**

- **Cause**: Required Python packages are not installed.
- **Solution**:
  1. Make sure you have activated your virtual environment.
  2. Install all dependencies:
     ```bash
     pip install -r requirements.txt
     ```

## 📂 PCAP File Issues

**1. "Error loading packets"**

- **Cause**: The PCAP file is corrupted or in an unsupported format.
- **Solution**:
  - Ensure your file is a valid `.pcap` or `.pcapng` file.
  - Try opening the file in Wireshark to verify its integrity.

## 🤖 AI Analysis Issues

**1. "AI response is empty or nonsensical"**

- **Cause**: The AI model may not have understood the query or the provided data.
- **Solution**:
  - Try rephrasing your question to be more specific.
  - Check the packet summary to ensure the data being sent to the AI is correct.

If you continue to experience issues, please consider opening an issue on the project's GitHub page.

# 🔧 Sniff Recon Troubleshooting Guide

## Common Issues and Solutions

### 1. AI Analysis Error: "API request failed: 404"

**Problem**: The Hugging Face API key is invalid or missing.

**Solution**:
1. Run the API key setup script:
   ```bash
   python setup_api_key.py
   ```

2. Or manually update your `.env` file:
   ```env
   HUGGINGFACE_API_KEY=your_new_api_key_here
   ```

3. Get a free API key from [Hugging Face](https://huggingface.co/settings/tokens)

**Note**: The app will still work with local analysis even without a valid API key.

### 2. Streamlit JavaScript Error

**Problem**: `TypeError: error loading dynamically imported module: http://localhost:8501/static/js/index.bwA9_eWC.js`

**Solutions**:
1. Update dependencies:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. Clear Streamlit cache:
   ```bash
   streamlit cache clear
   ```

3. Restart the application:
   ```bash
   streamlit run sniff_recon_gui.py
   ```

### 3. Import Errors

**Problem**: Missing dependencies or import errors.

**Solution**:
1. Install all requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. If using a virtual environment, activate it first:
   ```bash
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

### 4. File Upload Issues

**Problem**: Cannot upload or parse packet files.

**Solutions**:
1. Ensure file format is supported: `.pcap`, `.pcapng`, `.csv`, `.txt`
2. Check file permissions
3. Verify file is not corrupted

### 5. Performance Issues

**Problem**: Slow loading or analysis.

**Solutions**:
1. Use smaller packet files for testing
2. Close other applications to free up memory
3. Consider using the CLI version for large files

## Getting Help

If you encounter other issues:

1. Check the console output for error messages
2. Ensure all dependencies are installed
3. Try running the CLI version: `python cli_ai.py`
4. Check the logs in the application output

## API Key Setup

### Quick Setup
```bash
python setup_api_key.py
```

### Manual Setup
1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. Create a new token with "Read" permissions
3. Copy the token
4. Add it to your `.env` file:
   ```env
   HUGGINGFACE_API_KEY=hf_your_token_here
   ```

## Supported File Formats

- **PCAP/PCAPNG**: Wireshark capture files
- **CSV**: Network log exports
- **TXT**: Plain text network logs

## System Requirements

- Python 3.8+
- 4GB+ RAM (for large packet files)
- Internet connection (for AI features)
- Supported OS: Windows, macOS, Linux 