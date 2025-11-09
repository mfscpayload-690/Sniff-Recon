# 🔍 Sniff Recon v1.1.0 - "Protocol Cards & Multi-Provider AI"

## 🚀 Major UI/UX Overhaul and Enhanced AI Capabilities

**Release Date**: November 9, 2025  
**Commits Since v1.0.0**: 70+ commits  
**Contributors**: [Aravind Lal](https://github.com/mfscpayload-690), [Devu Krishna](https://github.com/krizzdev7)

---

## 🎨 Major Features

### 1. **Modern Protocol Layer Analysis UI**
- **Responsive Card Grid Layout**: Protocol layers now display as interactive cards instead of vertical lists
- **Neon Borders & Glow Effects**: Cyberpunk-themed visual enhancements with hover animations
- **Improved Readability**: Enhanced font hierarchy, contrast, and spacing for better data visibility
- **Fade-in Animations**: Smooth card entry animations for a polished user experience

### 2. **Google Gemini AI Provider Support**
- Added Google Gemini as the 4th AI provider (joining Groq, OpenAI, Anthropic)
- Explicit `.env` loading from Docker mounted paths for seamless configuration
- Provider status indicators show real-time connection health

### 3. **Quick Access Sidebar**
- **Quick Start Guide**: Interactive tutorial for new users
- **Documentation**: In-app access to setup guides and troubleshooting
- **Settings Panel**: Centralized configuration management with provider selection
- **Visual Icons**: Enhanced provider configuration section with status badges

### 4. **Advanced Packet Filtering**
- Filter by IP address (source/destination)
- Filter by protocol type (TCP, UDP, ICMP, etc.)
- Filter by port ranges
- Time-based filtering for large captures

### 5. **Session Management**
- **Export Sessions**: Save AI analysis sessions as JSON with full context
- **Import Sessions**: Resume previous analysis sessions with preserved history
- Dataclass serialization improvements for reliable export/import

### 6. **Professional PDF Export**
- Export AI analysis reports as formatted PDF documents
- Includes charts, summaries, and detailed insights
- Publication-ready formatting for reports and presentations

---

## 🔧 AI & Backend Improvements

### Multi-Agent AI Enhancements
- **Weighted Load Balancing**: Intelligent request distribution across providers based on performance
- **Random Provider Shuffling**: Prevents provider overload during high traffic
- **Provider Failover**: Automatic fallback to backup providers on API failures
- **Detailed Error Logging**: Comprehensive multi-agent failure diagnostics
- **Packet Data Fix**: Corrected empty packet list passing to AI agents

### Parser & Data Processing
- **PCAPNG Support**: Fixed critical parsing issues with PCAPNG files
- **JSON Serialization**: Improved handling of dataclasses and custom types (AIResponse, EDecimal)
- **Type Hints Cleanup**: Suppressed linter warnings and improved code quality

---

## 🐛 Bug Fixes

### UI Fixes
- Removed redundant headings for cleaner interface
- Fixed "SELECTED PACKET ANALYSIS" duplicate heading
- Improved text visibility for file uploader and info boxes
- Repositioned help content above file uploader for better UX
- Fixed Streamlit deprecation warnings (st.beta_expander → st.expander)

### Backend Fixes
- Resolved Groq model API compatibility issues
- Fixed corrupted `sniff_recon_gui.py` with About/Help popup restoration
- Corrected import path issues after src/ restructuring
- Fixed Help sidebar selectbox implementation

---

## 📁 Architecture & Refactoring

### Production-Ready Structure
- **Moved to `src/` Layout**: Organized code into `src/ai/`, `src/ui/`, `src/parsers/`, `src/utils/`
- **Removed Duplicate Root Files**: Cleaned up legacy files moved to src/ in v2.0.0
- **Docker-First Deployment**: Enhanced Dockerfile with improved module imports and error handling
- **Kubernetes Manifests**: Added bridge/ directory with Kustomize configs (ignored in git)

### Documentation Overhaul
- **CONTRIBUTING.md**: GitHub-ready contribution guidelines
- **SECURITY.md**: Security policy and vulnerability reporting
- **ROADMAP.md**: Realistic feature roadmap with timelines
- **Docker Guides**: Comprehensive Docker deployment, workflow, and troubleshooting docs
- **UI Development Workflow**: Developer guide for front-end-test branch
- **Quick Reference**: Cheat sheet for common UI development tasks
- **Weighted Balancing Guide**: Technical documentation for AI load balancing

---

## 🎨 Visual & UX Enhancements

### Animations & Effects
- **Particle Starfield Background**: Animated background for immersive UI
- **Matrix-Style Typewriter Effect**: One-time tagline animation on load
- **Neon Title**: Glowing cyberpunk-themed header
- **About/Help Popups**: Interactive modals with typewriter text effects

### Layout & Navigation
- Cleaner tab organization (Packet Analysis, AI Analysis, Export)
- Responsive design improvements for smaller screens
- Improved sidebar layout with collapsible sections

---

## 🐳 Docker & Deployment

### Docker Improvements
- Cleanup of outdated Docker files
- Removed Docker start/stop scripts (use `docker-compose` directly)
- Enhanced security with non-root user and minimal base image
- Mounted `.env` support for AI provider configuration

### Git & Repository Management
- `.gitignore` updates: Ignore `output/summary.json`, Kubernetes manifests
- Added `output/.gitkeep` to preserve directory structure
- Fixed repository URL in README for accurate cloning instructions

---

## 📊 What's Changed (By the Numbers)

- **70+ commits** since v1.0.0
- **4 AI providers** (Groq, OpenAI, Anthropic, Gemini)
- **10+ documentation files** added/updated
- **3 major UI redesigns** (Protocol Cards, Quick Access, Session Management)
- **15+ bug fixes** across UI, AI, and parsers
- **2 contributors** (Aravind Lal, Devu Krishna)

---

## 🚀 Quick Start

### Using Docker (Recommended)
```bash
# Option 1: Pull pre-built image from GitHub Container Registry
docker pull ghcr.io/mfscpayload-690/sniff-recon:1.1.0
docker run -d -p 8501:8501 --name sniff-recon ghcr.io/mfscpayload-690/sniff-recon:1.1.0

# Option 2: Build from source with docker-compose
docker-compose up -d

# Access at http://localhost:8501
```

### Local Installation
```bash
# Clone the repository
git clone https://github.com/mfscpayload-690/Sniff-Recon.git
cd Sniff-Recon

# Setup virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Launch GUI
python scripts/start_gui.py
# or
streamlit run src/ui/gui.py
```

---

## 🔄 Upgrade Notes

### Breaking Changes
- **None**: v1.1.0 is fully backward-compatible with v1.0.0

### Recommended Actions
1. **Update Environment Variables**: Add `GOOGLE_API_KEY` if using Gemini
2. **Docker Users**: Pull the latest image and restart containers
3. **Local Users**: Pull latest code and run `pip install -r requirements.txt`
4. **Review Settings**: Check the new Quick Access → Settings panel for provider configuration

### Migration from v1.0.0
No migration required! Simply update and enjoy the new features.

---

## 📦 Installation

See [Quick Start](#-quick-start) section above for installation instructions.

---

## 🔍 Verification

### Health Checks
- ✅ All tests passing on commit `ce6f282`
- ✅ Docker image built successfully
- ✅ UI tested with Chrome, Firefox, Edge
- ✅ AI providers tested (Groq, OpenAI, Anthropic, Gemini)
- ✅ PCAP/PCAPNG/CSV/TXT parsing verified

### Rollback Instructions
If you encounter issues:
```bash
# Git users
git checkout v1.0.0

# Docker users
docker-compose down
git checkout v1.0.0
docker-compose up -d
```

---

##  Full Changelog

For a detailed list of all commits, see:
```bash
git log v1.0.0..v1.1.0 --oneline
```

Or view on GitHub: [v1.0.0...v1.1.0](https://github.com/mfscpayload-690/Sniff-Recon/compare/v1.0.0...v1.1.0)

---

**Enjoy the enhanced Sniff Recon experience! 🔍📊✨**

*Questions or issues? Open a [GitHub Issue](https://github.com/mfscpayload-690/Sniff-Recon/issues) or check the [Documentation](https://github.com/mfscpayload-690/Sniff-Recon/tree/main/docs).*
