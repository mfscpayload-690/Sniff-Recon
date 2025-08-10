# syntax=docker/dockerfile:1
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port for Streamlit GUI (optional)
EXPOSE 8501

# Default entrypoint: Enhanced CLI (change to sniff_recon_gui.py for GUI)
CMD ["streamlit", "run", "sniff_recon_gui.py"]
