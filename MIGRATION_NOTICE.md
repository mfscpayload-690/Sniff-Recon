# 🔄 Migration Notice - CLI Removed

## What Changed?

This version of Sniff Recon has been **simplified to GUI-only**. All CLI (Command Line Interface) components have been removed to focus on providing the best possible graphical user experience.

## Removed Components

The following CLI files have been removed:
- `main.py` - Original CLI parser
- `cli_ai.py` - CLI AI interface  
- `enhanced_cli_ai.py` - Enhanced CLI with multi-agent support
- `setup_api_key.py` - CLI setup script
- `setup_multi_agent.py` - Multi-agent setup script
- `test_ai_function.py` - Testing scripts
- `test_hf_api.py` - API testing scripts

## What You Get Instead

✅ **Modern Web-Based GUI** - Beautiful, responsive interface  
✅ **Drag & Drop File Upload** - Easy file handling  
✅ **Interactive Analysis** - Real-time charts and tables  
✅ **AI-Powered Insights** - Natural language queries (optional)  
✅ **Export Capabilities** - Download results as JSON  
✅ **Beautiful Dark Theme** - Modern cyberpunk design  

## How to Use the New Version

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Launch the GUI (recommended)
python start_gui.py

# Or start directly with Streamlit
streamlit run sniff_recon_gui.py
```

### Access the Application
- Open your web browser
- Go to `http://localhost:8501`
- Upload your packet capture files
- Enjoy the modern interface!

## Need the CLI Version?

If you specifically need CLI functionality, you can:
1. Use the previous version of this repository (check git history)
2. Use standard networking tools like `tshark`, `tcpdump`, or `wireshark`
3. Build your own CLI wrapper around the existing parser modules

## Questions?

Check out:
- `README.md` - Complete setup and usage guide
- `SETUP.md` - Detailed setup instructions  
- `TROUBLESHOOTING.md` - Common issues and solutions

**Happy Network Analysis! 🔍📊**
