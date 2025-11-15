# 🛠️ Sniff Recon GUI - Troubleshooting Guide

This guide helps resolve common issues with Sniff Recon's GUI application.

## 🔑 API Key and Configuration Issues

**1. "API Key not found" or AI features not working**

- **Cause**: The application cannot find your AI provider API keys.
- **Solution**:
  1. Create a `.env` file in the project root directory
  2. Add your API keys:
     ```env
     GROQ_API_KEY=your_groq_key_here
     OPENAI_API_KEY=your_openai_key_here
     ```
  3. Restart the Streamlit application

**2. "Invalid API key" errors**

- **Cause**: The API key is incorrect or has been revoked.
- **Solution**:
  1. Get a new key from the respective provider:
     - Groq: [https://console.groq.com/keys](https://console.groq.com/keys)
     - OpenAI: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
  2. Update your `.env` file with the new key
  3. Restart the application

**3. "Failed to parse .env file"**

- **Cause**: The `.env` file is formatted incorrectly.
- **Solution**:
  - Make sure each line contains `PROVIDER_API_KEY=your_key_here`
  - No spaces around the equals sign
  - Delete and recreate the file if needed

## 🌐 Network and API Connectivity Issues

**1. "API request failed with status 401: Unauthorized"**

- **Cause**: Your API key is invalid.
- **Solution**: Follow the steps for "Invalid API key" above.

**2. "API request failed with status 429: Rate Limit Exceeded"**

- **Cause**: You have exceeded the rate limits for your AI provider.
- **Solution**:
  - Wait a few minutes and try again
  - Check your provider's documentation for rate limit information
  - Consider upgrading to a paid plan if needed

**3. "Request error: Connection timed out"**

- **Cause**: Cannot connect to the AI provider's servers.
- **Solution**:
  - Check your internet connection
  - Ensure firewall/proxy isn't blocking API requests
  - Try again later if the service is down

## 📦 Dependencies and GUI Issues

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
   # Using the launcher script
   python scripts/start_gui.py
   
   # Or directly with Streamlit
   streamlit run app.py
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
3. Restart the Streamlit application
4. Try using a different browser

### 6. GUI Not Loading

**Problem**: Streamlit application won't start or load.

**Solutions**:
1. Check that port 8501 is available:
   ```bash
   lsof -i :8501  # Linux/Mac
   netstat -an | findstr :8501  # Windows
   ```
2. Try a different port:
   ```bash
   streamlit run app.py --server.port 8502
   ```
3. Clear browser cache and cookies
4. Try accessing directly: `http://localhost:8501`

## Getting Help

If you encounter other issues:

1. Check the Streamlit console output for error messages
2. Ensure all dependencies are installed correctly
3. Verify file permissions and formats
4. Check the application logs in the terminal

## Supported File Formats

- **PCAP/PCAPNG**: Wireshark capture files
- **CSV**: Network log exports
- **TXT**: Plain text network logs

## System Requirements

- Python 3.8+
- 4GB+ RAM (for large packet files)
- Internet connection (for AI features)
- Supported OS: Windows, macOS, Linux 