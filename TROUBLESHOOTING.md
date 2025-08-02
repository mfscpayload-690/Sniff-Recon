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