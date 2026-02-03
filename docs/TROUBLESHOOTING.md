# Troubleshooting Guide

Common issues and solutions for Sniff-Recon.

---

## Table of Contents

- [Installation Issues](#installation-issues)
- [Ollama Issues](#ollama-issues)
- [AI Provider Issues](#ai-provider-issues)
- [File Upload Issues](#file-upload-issues)
- [Docker Issues](#docker-issues)
- [Performance Issues](#performance-issues)
- [Common Errors](#common-errors)

---

## Installation Issues

### ModuleNotFoundError: No module named 'scapy'

**Cause**: Dependencies not installed or venv not activated

**Solution**:

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Permission denied (libpcap)

**Cause**: Scapy needs rawSocket access for some operations

**Solution** (Linux):

```bash
# Run with sudo (not recommended for production)
sudo streamlit run app.py

# OR: Give Python capabilities (better)
sudo setcap cap_net_raw,cap_net_admin+eip $(which python)
```

For analysis of PCAP files (not live capture), sudo is NOT needed.

---

## Ollama Issues

### "Cannot connect to Ollama"

**Cause**: Ollama daemon not running

**Solution**:

```bash
# Check if Ollama is running
pgrep -f ollama

# If not, start it
ollama serve

# In background:
nohup ollama serve > /tmp/ollama.log 2>&1 &
```

**Verify connection**:

```bash
curl http://localhost:11434/api/tags
# Should return JSON with models
```

### "Ollama (Local)" not appearing in dropdown

**Cause**: Ollama not enabled or failed connection test

**Solution**:

1. **Check `.env`**:

   ```bash
   OLLAMA_ENABLED=true
   OLLAMA_BASE_URL=http://localhost:11434
   ```

2. **Verify Ollama running**:

   ```bash
   curl http://localhost:11434/api/tags
   ```

3. **Check logs**:

   ```bash
   tail -f sniff_recon.log | grep -i ollama
   ```

4. **Restart Sniff-Recon**

### "Model 'qwen2.5-coder:7b' not found"

**Cause**: Model not downloaded

**Solution**:

```bash
# List installed models
ollama list

# Download missing model
ollama pull qwen2.5-coder:7b

# Verify
ollama list | grep qwen
```

### Ollama request timed out (>120s)

**Cause**: Model too large for hardware or system overloaded

**Solutions**:

1. **Use smaller model**:

   ```bash
   ollama pull qwen2.5-coder:1.5b
   # Update .env: OLLAMA_MODEL=qwen2.5-coder:1.5b
   ```

2. **Reduce chunk size** (edit `.env`):

   ```bash
   CHUNK_SIZE_MB=3
   MAX_PACKETS_PER_CHUNK=2000
   ```

3. **Close other applications** to free RAM

4. **Check GPU usage** (if available):

   ```bash
   nvidia-smi  # NVIDIA
   rocm-smi    # AMD
   ```

### Very slow Ollama inference (30+ seconds)

**Cause**: CPU-only inference on weak hardware

**Solutions**:

1. **Check GPU acceleration**:

   ```bash
   # NVIDIA
   nvidia-smi
   # During query, GPU usage should spike

   # AMD
   rocm-smi
   ```

2. **Use quantized model**:

   ```bash
   ollama pull qwen2.5-coder:7b-q4_0
   # Smaller, faster
   ```

3. **Switch to cloud AI** for better performance

---

## AI Provider Issues

### "No active AI providers available"

**Cause**: No valid API keys or Ollama not running

**Solution**:

1. **For Cloud AI**:

   ```bash
   # Check .env has valid keys
   cat .env | grep API_KEY
   ```

2. **For Ollama**:

   ```bash
   # Start Ollama
   ollama serve &
   ```

3. **Check provider status**:

   ```python
   from src.ai.multi_agent_ai import get_active_providers
   print(get_active_providers())
   ```

### "Groq API rate limit exceeded"

**Cause**: Free tier limits hit

**Solutions**:

1. **Wait** (limits reset periodically)
2. **Add another provider**:

   ```bash
   # Edit .env
   OPENAI_API_KEY=sk-...
   GOOGLE_API_KEY=AIza...
   ```

3. **Use Ollama** (no rate limits)

### "Invalid API key" errors

**Cause**: Incorrect or expired API key

**Solution**:

1. **Verify key format**:
   - Groq: `gsk_...`
   - OpenAI: `sk-...`
   - Anthropic: `sk-ant-...`
   - Google: `AIza...`
   - xAI: `xai-...`

2. **Regenerate key** from provider dashboard

3. **Check for typos** in `.env`

4. **Restart app** after updating `.env`

---

## File Upload Issues

### File upload fails silently

**Cause**: File too large or invalid format

**Solution**:

1. **Check file size**:

   ```bash
   ls -lh your-file.pcap
   # Should be <200MB (default limit)
   ```

2. **Increase limit** (edit `.env`):

   ```bash
   MAX_FILE_SIZE_MB=500
   ```

3. **Verify file format**:

   ```bash
   file your-file.pcap
   # Should say "tcpdump capture file"
   ```

### "Unable to parse PCAP file"

**Cause**: Corrupted or malformed PCAP

**Solution**:

1. **Verify with tshark**:

   ```bash
   tshark -r your-file.pcap -c 10
   ```

2. **Try repairing**:

   ```bash
   tcpdump -r broken.pcap -w fixed.pcap
   ```

3. **Check PCAP version** (some very old formats unsupported)

### CSV parsing fails

**Cause**: CSV missing required columns

**Solution**:

Required columns: `Source IP`, `Destination IP`, `Protocol`

Example valid CSV:

```csv
Source IP,Destination IP,Protocol,Source Port,Destination Port
192.168.1.1,8.8.8.8,TCP,5555,443
```

---

## Docker Issues

### docker-compose: command not found

**Cause**: Docker Compose not installed

**Solution**:

```bash
# Linux
sudo apt install docker-compose

# Or use docker compose (plugin)
docker compose up -d
```

### Permission denied (Docker socket)

**Cause**: User not in docker group

**Solution**:

```bash
sudo usermod -aG docker $USER
# Logout and login again
```

### Container not starting

**Cause**: Port 8501 already in use

**Solution**:

1. **Check port usage**:

   ```bash
   sudo lsof -i :8501
   ```

2. **Kill process or use different port**:

   ```bash
   # Edit docker-compose.yml
   ports:
     - "8080:8501"  # Changed from 8501:8501
   ```

### Cannot access Ollama from Docker container

**Cause**: Network isolation

**Solution**:

```yaml
# docker-compose.yml
services:
  sniff-recon:
    network_mode: "host"  # Allow access to host's localhost
    # OR use separate Ollama container
```

See [DOCKER.md](DOCKER.md) for Ollama + Docker setup.

---

## Performance Issues

### App is very slow / freezing

**Cause**: Large PCAP file or insufficient RAM

**Solutions**:

1. **Reduce file size**:

   ```bash
   # Split PCAP into smaller chunks
   tcpdump -r large.pcap -w small.pcap -c 10000
   ```

2. **Adjust chunk settings** (`.env`):

   ```bash
   CHUNK_SIZE_MB=3
   MAX_PACKETS_PER_CHUNK=3000
   ```

3. **Close other apps** to free RAM

4. **Use CLI for very large files** (bypass UI):

   ```python
   from src.parsers.pcap_parser import parse_pcap
   df = parse_pcap("huge.pcap")
   ```

### High CPU usage

**Cause**: Multiple AI queries or large file parsing

**Expected**: CPU spikes during:

- PCAP parsing (Scapy)
- AI inference (Ollama)
- Suspicious packet filtering

**Not a bug** unless sustained >80% when idle.

---

## Common Errors

### StreamlitAPIException: st.session_state cannot be modified

**Cause**: Trying to modify session state during callback

**Fix**: Contact developers (this is a code bug)

### AttributeError: 'NoneType' object has no attribute 'src'

**Cause**: Packet missing expected layer (e.g., no IP layer)

**Fix**: This is handled in code, but if you see it:

```python
# Always check layer presence
if IP in pkt:
    src_ip = pkt[IP].src
```

### ImportError: cannot import name 'X' from 'scapy'

**Cause**: Scapy version mismatch

**Solution**:

```bash
pip install --upgrade scapy==2.5.0
```

---

## Still Stuck?

### Debug Mode

Enable detailed logging:

```bash
# Edit .env
DEBUG_LOGGING=true
LOG_LEVEL=DEBUG

# Run app
streamlit run app.py

# Check logs
tail -f sniff_recon.log
```

### Report an Issue

If problem persists:

1. **Gather information**:
   - OS and version
   - Python version: `python --version`
   - Sniff-Recon version: `git describe --tags`
   - Error logs from `sniff_recon.log`

2. **Create GitHub issue**: [github.com/mfscpayload-690/Sniff-Recon/issues](https://github.com/mfscpayload-690/Sniff-Recon/issues)

3. **Include**:
   - Steps to reproduce
   - Expected vs actual behavior
   - Sample PCAP (if applicable, remove sensitive data)
   - Logs

---

## Quick Reference

### Reset Everything

```bash
# Stop all services
pkill ollama
docker-compose down

# Remove venv
rm -rf venv

# Fresh install
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Restart
ollama serve &
streamlit run app.py
```

### Check System Status

```bash
# Python dependencies
pip list | grep -E 'streamlit|scapy|pandas'

# Ollama status
curl http://localhost:11434/api/tags

# Docker status
docker-compose ps

# Port usage
sudo lsof -i :8501
```

---

**Last Updated**: February 2026  
**Sniff-Recon Version**: 1.2.0+
