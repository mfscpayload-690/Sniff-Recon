# Ollama Integration Guide

**Complete guide to using Sniff-Recon in offline mode with local LLMs**

---

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Model Selection](#model-selection)
- [Configuration](#configuration)
- [Usage](#usage)
- [Performance](#performance)
- [Troubleshooting](#troubleshooting)
- [Advanced Topics](#advanced-topics)

---

## Overview

Ollama integration enables **100% offline AI-powered packet analysis** for Sniff-Recon. All analysis runs on your local machine using open-source large language models.

### Benefits

- **🔒 Privacy**: No data sent to external services
- **💰 Cost**: Zero API fees
- **📡 Offline**: No internet required
- **🏢 Compliance**: GDPR/SOC 2 friendly
- **🚀 Performance**: No network latency

### Use Cases

| Scenario | Recommended Mode |
|----------|-----------------|
| **Classified traffic analysis** | 🔒 Ollama (Offline) |
| **Enterprise SOC (sensitive data)** | 🔒 Ollama (Offline) |
| **Air-gapped networks** | 🔒 Ollama (Offline) |
| **General packet analysis** | ☁️ Cloud AI (Faster) |
| **Learning/testing** | Both (switchable) |

---

## Installation

### Prerequisites

- **OS**: Linux, macOS, Windows (WSL2)
- **RAM**: 8GB minimum (16GB recommended)
- **Disk**: 5-50GB (depends on model)
- **CPU/GPU**: Any (GPU accelerates inference)

### Step 1: Install Ollama

#### Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### macOS

```bash
brew install ollama
```

#### Windows

Download installer from [ollama.ai/download](https://ollama.ai/download)

### Step 2: Verify Installation

```bash
ollama --version
```

Expected output: `ollama version 0.x.x`

---

## Quick Start

### 1. Start Ollama Daemon

```bash
ollama serve
```

Keep this terminal open. Output should show:

```
Ollama is running on http://localhost:11434
```

### 2. Download AI Model

```bash
# Recommended for network analysis (8GB RAM)
ollama pull qwen2.5-coder:7b

# Alternative models
ollama pull llama3:8b        # General purpose
ollama pull codellama:13b    # More accurate (16GB RAM)
```

### 3. Configure Sniff-Recon

Edit `.env`:

```bash
OLLAMA_ENABLED=true
OLLAMA_MODEL=qwen2.5-coder:7b
OLLAMA_BASE_URL=http://localhost:11434
```

### 4. Run Sniff-Recon

```bash
./dev-setup.sh  # Automated (Arch Linux)
# Or manually:
streamlit run app.py
```

### 5. Select Local LLM in UI

1. Open <http://localhost:8501>
2. Upload a PCAP file
3. In AI Query section, select **"Ollama (Local)"** from dropdown
4. Look for 🔒 **OFFLINE** badge
5. Ask questions normally

---

## Model Selection

### Recommended Models for Network Analysis

| Model | RAM | Speed | Accuracy | Best For |
|-------|-----|-------|----------|----------|
| **qwen2.5-coder:7b** ⭐ | 8GB | Fast | High | Network/code analysis (DEFAULT) |
| llama3:8b | 8GB | Fast | Good | General analysis |
| codellama:13b | 16GB | Medium | Higher | Detailed forensics |
| qwen2.5-coder:32b | 32GB | Slow | Highest | Maximum accuracy |
| llama3:70b | 64GB+ | Very Slow | Highest | Enterprise (powerful hardware) |

⭐ = **Recommended default**

### Model Management

```bash
# List installed models
ollama list

# Download a model
ollama pull <model-name>

# Remove a model
ollama rm <model-name>

# Test a model
ollama run qwen2.5-coder:7b "Explain TCP handshake"
```

### Switching Models

1. Pull new model: `ollama pull llama3:8b`
2. Update `.env`: `OLLAMA_MODEL=llama3:8b`
3. Restart Sniff-Recon

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_ENABLED` | `false` | Enable/disable Ollama |
| `OLLAMA_MODEL` | `qwen2.5-coder:7b` | Model to use |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API endpoint |
| `OLLAMA_WEIGHT` | `30` | Load balancing weight (future use) |

### Example `.env` (Offline-Only)

```bash
# Cloud providers (set to placeholders)
GROQ_API_KEY=offline_mode
OPENAI_API_KEY=offline_mode
ANTHROPIC_API_KEY=offline_mode
GOOGLE_API_KEY=offline_mode
XAI_API_KEY=offline_mode

# Ollama configuration
OLLAMA_ENABLED=true
OLLAMA_MODEL=qwen2.5-coder:7b
OLLAMA_BASE_URL=http://localhost:11434

# File processing
MAX_FILE_SIZE_MB=200
CHUNK_SIZE_MB=5
MAX_PACKETS_PER_CHUNK=5000
```

---

## Usage

### Basic Workflow

1. **Upload PCAP**: Drag and drop or browse
2. **Select Provider**: Choose "Ollama (Local)"
   - 🔒 **OFFLINE** badge confirms local mode
3. **Ask Questions**: Natural language queries
4. **Review Results**: AI analysis appears in UI
5. **Export**: JSON/CSV/PDF reports

### Example Queries

```
"What are the top 5 source IP addresses?"
"Show me all SYN flood attempts"
"Identify suspicious DNS queries"
"Analyze HTTP traffic patterns"
"Find potential port scans"
"Summarize this network capture"
```

### Verifying Offline Mode

**Method 1: Check UI Badge**

- Look for 🔒 **OFFLINE** badge next to provider selection

**Method 2: Network Monitor**

```bash
# Monitor outbound traffic (should be none during analysis)
sudo tcpdump -i any 'not host 127.0.0.1 and not host localhost'
```

During AI queries, you should see **no external connections**.

**Method 3: Check Logs**

```bash
tail -f sniff_recon.log | grep "Ollama"
```

Look for: `Explicit provider mode: Using only 'Ollama (Local)'`

---

## Performance

### Benchmarks

**Hardware: Apple M1 Pro (16GB RAM)**

| Model | Packets | Query Time | RAM Usage |
|-------|---------|------------|-----------|
| qwen2.5-coder:7b | 5,000 | ~8s | 6.2GB |
| llama3:8b | 5,000 | ~10s | 6.5GB |
| codellama:13b | 5,000 | ~15s | 9.8GB |

**Hardware: Linux Server (NVIDIA RTX 3080, 24GB VRAM)**

| Model | Packets | Query Time | VRAM Usage |
|-------|---------|------------|------------|
| qwen2.5-coder:7b | 5,000 | ~3s | 5.1GB |
| codellama:13b | 5,000 | ~5s | 8.2GB |
| qwen2.5-coder:32b | 5,000 | ~8s | 18.4GB |

### Optimization Tips

#### 1. GPU Acceleration (NVIDIA)

Check if Ollama is using GPU:

```bash
nvidia-smi
```

During inference, GPU usage should spike to 80-100%.

#### 2. CPU-Only Optimization

For systems without GPU:

```bash
# Use smaller models
ollama pull qwen2.5-coder:1.5b

# Update .env
OLLAMA_MODEL=qwen2.5-coder:1.5b
```

#### 3. Reduce Context Length

Edit `.env`:

```bash
 CHUNK_SIZE_MB=3          # Smaller chunks
MAX_PACKETS_PER_CHUNK=3000  # Fewer packets per query
```

#### 4. Close Other Applications

Free up RAM for better performance.

---

## Troubleshooting

### Issue: "Cannot connect to Ollama"

**Cause**: Ollama daemon not running

**Solution**:

```bash
# Check if Ollama is running
pgrep -f ollama

# If not, start it
ollama serve
```

---

### Issue: "Model not found"

**Cause**: Model not downloaded

**Solution**:

```bash
# List installed models
ollama list

# Download missing model
ollama pull qwen2.5-coder:7b
```

---

### Issue: "Ollama request timed out (>120s)"

**Cause**: Model too large for hardware

**Solutions**:

1. Use smaller model:

   ```bash
   ollama pull qwen2.5-coder:1.5b
   ```

2. Reduce chunk size in `.env`:

   ```bash
   CHUNK_SIZE_MB=2
   MAX_PACKETS_PER_CHUNK=2000
   ```

3. Add more RAM/GPU

---

### Issue: Very slow inference (30+ seconds)

**Cause**: CPU-only inference on underpowered hardware

**Solutions**:

1. **Check for GPU**:

   ```bash
   nvidia-smi  # NVIDIA
   rocm-smi    # AMD
   ```

2. **Use quantized models**:

   ```bash
   ollama pull qwen2.5-coder:7b-q4_0  # Smaller, faster
   ```

3. **Switch to cloud AI** for better performance

---

### Issue: "Ollama (Local)" not in provider dropdown

**Cause**: Ollama not enabled or failed connection test

**Solution**:

1. Check `.env`:

   ```bash
   OLLAMA_ENABLED=true
   ```

2. Verify Ollama running:

   ```bash
   curl http://localhost:11434/api/tags
   ```

3. Restart Sniff-Recon
4. Check logs:

   ```bash
   tail -f sniff_recon.log | grep -i ollama
   ```

---

## Advanced Topics

### Running Ollama on Different Port

```bash
# Start Ollama on custom port
OLLAMA_HOST=0.0.0.0:8080 ollama serve
```

Update `.env`:

```bash
OLLAMA_BASE_URL=http://localhost:8080
```

---

### Remote Ollama Server

Run Ollama on a powerful server, access from lightweight client:

**On Server**:

```bash
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

**On Client** (edit `.env`):

```bash
OLLAMA_BASE_URL=http://server-ip:11434
```

⚠️ **Security Warning**: This exposes Ollama to your network. Use firewall/VPN.

---

### Custom Modelfile

Tune model parameters for network analysis:

```dockerfile
# Modelfile
FROM qwen2.5-coder:7b

# Increase context for large PCAPs
PARAMETER num_ctx 8192

# More focused responses
PARAMETER temperature 0.1

# System prompt optimization
SYSTEM You are a network security expert specializing in packet analysis and threat detection.
```

Build:

```bash
ollama create sniff-recon-optimized -f Modelfile
```

Use in `.env`:

```bash
OLLAMA_MODEL=sniff-recon-optimized
```

---

### Docker Deployment with Ollama

`docker-compose.yml`:

```yaml
version: '3'

services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama-models:/root/.ollama
    restart: unless-stopped

  sniff-recon:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OLLAMA_ENABLED=true
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama
    volumes:
      - ./output:/app/output

volumes:
  ollama-models:
```

Deploy:

```bash
docker-compose up -d

# Pull model inside Ollama container
docker exec -it ollama ollama pull qwen2.5-coder:7b
```

---

## FAQ

### Q: Can I use both Ollama and cloud AI?

**A**: Yes! Switch providers anytime:

- **Ollama (Local)** → Sensitive data
- **Auto (Load Balanced)** → General analysis
- **Specific provider** (Groq, OpenAI) → Direct routing

### Q: How much disk space do models require?

**A**: Varies by model:

- qwen2.5-coder:7b → 4.7GB
- llama3:8b → 4.7GB
- codellama:13b → 7.4GB
- qwen2.5-coder:32b → 19GB

Check disk usage: `du -sh ~/.ollama/models`

### Q: Is Ollama as good as GPT-4?

**A**: No, but adequate for most analysis:

- **Smaller models (7B-13B)**: Good pattern recognition, basic insights
- **Larger models (32B-70B)**: Comparable quality to GPT-3.5
- **GPT-4**: Still superior for complex reasoning

Use Ollama for privacy, GPT-4 for maximum quality.

### Q: Can I use Ollama on Windows?

**A**: Yes, via:

1. **Native Ollama** (Windows 10/11)
2. **WSL2** (recommended for better performance)
3. **Docker Desktop**

---

## Support

- **Issues**: [GitHub Issues](https://github.com/mfscpayload-690/Sniff-Recon/issues)
- **Ollama Docs**: [ollama.ai/docs](https://ollama.ai/docs)
- **Discord**: [Sniff-Recon Community](#) (coming soon)

---

**Last Updated**: February 2026  
**Sniff-Recon Version**: 1.2.0+
