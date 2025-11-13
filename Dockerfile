# Use Python 3.11 (stable version with PyArrow support)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Scapy and network tools
# Apply security updates to fix vulnerabilities
RUN apt-get update && apt-get install -y \
    tcpdump \
    libpcap-dev \
    curl \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Add /app to PYTHONPATH so Python can import from src/
# No need to append to existing PYTHONPATH since base image doesn't set it
ENV PYTHONPATH="/app"

# Create output directory
RUN mkdir -p output

# Expose Streamlit port
EXPOSE 8501

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the application
# Run Streamlit using app.py as the entry point (imports from src/ui/gui.py)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
