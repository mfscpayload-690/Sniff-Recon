# =============================================================================
# Sniff-Recon Dockerfile
# =============================================================================
# Lightweight container that connects to host Ollama (or cloud AI)
# 
# For Ollama users: Run Ollama on host, container connects via network
# For Cloud users: Just add API keys to .env
# =============================================================================

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tcpdump \
    libpcap-dev \
    curl \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set Python path
ENV PYTHONPATH="/app"

# Create output directory
RUN mkdir -p output

# Streamlit configuration
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Ollama defaults (connects to host by default)
# On Linux: Use host.docker.internal or 172.17.0.1 (Docker gateway)
# Users can override via .env or docker-compose
ENV OLLAMA_ENABLED=true
ENV OLLAMA_MODEL=qwen2.5-coder:7b
ENV OLLAMA_BASE_URL=http://host.docker.internal:11434

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
