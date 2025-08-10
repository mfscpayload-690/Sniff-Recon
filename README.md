# 🐳 Docker Support for Sniff Recon

## 🚧 Coming Soon: Containerized Deployment

### Current Status: **Not Dockerized**

Sniff Recon v1.0.0 is currently designed to run directly on your host system using Python virtual environments. We've focused on delivering a stable, feature-rich GUI experience first.

### 🔮 Future Plans: Docker Integration

We're actively working on Docker containerization to provide:

- **🖥️ Cross-Platform Compatibility**: Seamless deployment on Linux, macOS, and Windows
- **📦 Isolated Environment**: No dependency conflicts with your host system  
- **⚡ One-Command Setup**: Simple `docker run` deployment
- **🔧 Consistent Experience**: Same behavior across all operating systems

### 📅 Timeline

Docker support is planned for **Sniff Recon v1.1.0** in the coming days/weeks.

### 🚀 Current Installation (Host-based)

Until Docker support arrives, please use the standard installation:

```bash
# Setup
python3 -m venv venv_gui
source venv_gui/bin/activate  # Linux/macOS
# venv_gui\Scripts\activate   # Windows

# Install & Run
pip install -r requirements.txt
./run_gui.sh  # Linux/macOS
# python start_gui.py         # Windows
```

### 💡 Why Containerize?

Docker will solve common issues like:
- Python version conflicts
- Dependency management across different systems
- Permission issues with packet capture files
- Simplified deployment for enterprise environments

### 📬 Stay Updated

Watch this repository for updates on Docker support! The containerized version will include:
- Multi-architecture support (AMD64, ARM64)
- Volume mounts for persistent data
- Environment variable configuration
- Health checks and logging

---

**⭐ Star this repo to get notified when Docker support lands!**
