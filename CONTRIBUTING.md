# Contributing to Sniff Recon

First off, thank you for considering contributing to Sniff Recon! 🎉 It's people like you that make this network packet analyzer better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Setting Up Development Environment](#setting-up-development-environment)

## Code of Conduct

This project adheres to a basic code of conduct: **Be respectful, be professional, and help each other learn.** We're all here to build something cool together.

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, Python version, Docker/local setup)
- **Sample PCAP files** (if the issue is file-specific)

### 💡 Suggesting Enhancements

Feature requests are welcome! Please include:

- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives considered**: Other ways you thought about solving this
- **Impact**: Who would benefit from this feature?

### 🔧 Code Contributions

We welcome code contributions! Areas where help is especially appreciated:

- **Parser improvements**: Better handling of edge cases in PCAP/CSV/TXT parsing
- **AI provider integrations**: Adding new LLM providers to the multi-agent system
- **UI enhancements**: Improving the Streamlit interface (cyberpunk theme 🌃)
- **Test coverage**: Writing unit tests for parsers and AI modules
- **Documentation**: Improving setup guides, troubleshooting, and inline code docs
- **Performance**: Optimizing packet filtering and clustering algorithms

## Development Workflow

### Branches

- **`main`**: Production-ready code, stable releases
- **`front-end-test`**: UI development and experiments (used by @devukrishna)
- **Feature branches**: `feature/your-feature-name` for new features
- **Bugfix branches**: `bugfix/issue-number-description` for bug fixes

### Workflow Steps

1. **Fork the repository** and clone your fork locally
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-awesome-feature
   ```
3. **Make your changes** following our coding standards (see below)
4. **Test your changes** locally (use `python scripts/start_gui.py` or Docker)
5. **Commit your changes** with descriptive messages (see commit guidelines)
6. **Push to your fork** and create a Pull Request
7. **Respond to review feedback** - we'll work together to get it merged!

## Coding Standards

### Python Style

- **PEP 8 compliant**: Use 4 spaces for indentation, 79-character line limit where reasonable
- **Type hints**: Always use type hints for function parameters and return values
  ```python
  # Good ✅
  def parse_pcap(file_path: str) -> pd.DataFrame:
      ...
  
  # Avoid ❌
  def parse_pcap(file_path):
      ...
  ```
- **Optional types**: Use `Optional[Type]` for nullable parameters
  ```python
  from typing import Optional
  
  def query(prompt: str, context: Optional[str] = None) -> str:
      ...
  ```
- **Docstrings**: Use Google-style docstrings for functions and classes
  ```python
  def filter_suspicious_packets(packets: list) -> list:
      """Filter packets based on suspicious patterns.
      
      Args:
          packets: List of Scapy packet objects to analyze
          
      Returns:
          List of packets matching suspicious criteria (SYN floods, port scans, etc.)
      """
  ```

### Project-Specific Patterns

- **Scapy layer checks**: ALWAYS check layer presence before accessing
  ```python
  # Good ✅
  if IP in pkt:
      src_ip = pkt[IP].src
  
  # Crashes ❌
  src_ip = pkt[IP].src  # Crashes if no IP layer!
  ```

- **Streamlit state management**: Clear temporary state before `st.rerun()`
  ```python
  # Good ✅
  st.session_state.user_query = query
  st.rerun()
  # Later, before next rerun:
  st.session_state.user_query = ""
  st.rerun()
  ```

- **Parser return format**: All parsers must return pandas DataFrames with standardized columns:
  - `Timestamp`, `Source IP`, `Destination IP`, `Protocol`, `Source Port`, `Destination Port`

- **AI provider integration**: New providers must subclass `AIProvider` in `src/ai/multi_agent_ai.py`

### File Organization

- **Parsers**: `src/parsers/` (simple functions, no classes)
- **AI modules**: `src/ai/` (multi-agent system, query functions)
- **UI components**: `src/ui/` (Streamlit pages, display functions)
- **Utilities**: `src/utils/` (shared helpers)
- **Scripts**: `scripts/` (Docker helpers, dev tools, start_gui.py)
- **Tests**: `tests/` (pytest test files)

## Commit Message Guidelines

We follow **Conventional Commits** for clear git history:

### Format
```
<type>(<scope>): <subject>

<body (optional)>

<footer (optional)>
```

### Types
- `feat`: New feature (e.g., `feat(ai): add Gemini provider support`)
- `fix`: Bug fix (e.g., `fix(parser): handle empty CSV files`)
- `docs`: Documentation only (e.g., `docs: update ROADMAP.md`)
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring (e.g., `refactor: restructure to src/ architecture`)
- `test`: Adding or updating tests
- `chore`: Build/tooling changes (e.g., `chore: update Docker config`)

### Examples
```bash
# Good ✅
git commit -m "feat(parser): add support for pcapng format"
git commit -m "fix(ui): improve text visibility in file uploader"
git commit -m "docs: add CONTRIBUTING and SECURITY guidelines"

# Avoid ❌
git commit -m "fixed stuff"
git commit -m "updated files"
```

## Pull Request Process

1. **Update documentation** if you've changed functionality
2. **Add tests** for new features (if applicable)
3. **Ensure all tests pass** locally before submitting
4. **Update ROADMAP.md** if your PR completes a roadmap item
5. **Fill out the PR template** with:
   - What does this PR do?
   - How to test it?
   - Related issues (if any)
   - Screenshots (for UI changes)

6. **Request review** from maintainers (@mfscpayload-690 or @devukrishna)
7. **Respond to feedback** - we'll iterate together until it's ready!

### PR Checklist
- [ ] Code follows PEP 8 and project conventions
- [ ] Type hints added for all functions
- [ ] Scapy layer checks used (if working with packets)
- [ ] Tested locally (both `python scripts/start_gui.py` and Docker)
- [ ] Documentation updated (if needed)
- [ ] Commit messages follow Conventional Commits
- [ ] No merge conflicts with `main`

## Setting Up Development Environment

### Local Python Setup (Recommended for development)

```powershell
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Sniff-Recon.git
cd Sniff-Recon

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
# or: source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the app
python scripts/start_gui.py
# or: streamlit run app.py
```

### Docker Setup (Testing production environment)

```powershell
# Build and run
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### AI Provider Setup (Optional)

Create `.env` file in project root:
```bash
GROQ_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

The app works without AI providers (provides fallback statistical analysis).

### Verifying Your Setup

```python
# Test parser in isolation
from src.parsers.pcap_parser import parse_pcap
df = parse_pcap("sample.pcap")
print(df.head())

# Check AI providers
from src.ai.multi_agent_ai import get_active_providers
providers = get_active_providers()
print(f"Active: {providers}")  # Should show connected providers
```

## Getting Help

- **Questions?** Open a [GitHub Discussion](https://github.com/mfscpayload-690/Sniff-Recon/discussions)
- **Found a bug?** Create an [Issue](https://github.com/mfscpayload-690/Sniff-Recon/issues)
- **Want to chat?** Reach out via GitHub (we're friendly! 😊)

## Recognition

Contributors will be:
- Listed in project README.md credits
- Mentioned in release notes for their contributions
- Given credit in commit history (ensure your git config is set correctly!)

---

**Thank you for contributing to Sniff Recon!** Every contribution, no matter how small, helps make network security tools more accessible. 🔒🚀
