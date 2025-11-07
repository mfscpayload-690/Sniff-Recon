# Sniff Recon - Docker Start Script
# This script builds and starts Sniff Recon in Docker

Write-Host "🔍 Starting Sniff Recon in Docker..." -ForegroundColor Cyan

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Stop any running instances
Write-Host "🛑 Stopping existing containers..." -ForegroundColor Yellow
docker-compose down 2>$null

# Build the image
Write-Host "🔨 Building Docker image..." -ForegroundColor Yellow
docker-compose build

# Start the container
Write-Host "🚀 Starting container..." -ForegroundColor Yellow
docker-compose up -d

# Wait a few seconds for startup
Start-Sleep -Seconds 5

# Check status
$status = docker ps --filter "name=sniff-recon-app" --format "{{.Status}}"
if ($status) {
    Write-Host "✅ Sniff Recon is running!" -ForegroundColor Green
    Write-Host "📡 Access at: http://localhost:8501" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Useful commands:" -ForegroundColor Yellow
    Write-Host "  View logs:    docker logs sniff-recon-app -f" -ForegroundColor Gray
    Write-Host "  Stop:         docker-compose down" -ForegroundColor Gray
    Write-Host "  Restart:      docker-compose restart" -ForegroundColor Gray
} else {
    Write-Host "❌ Failed to start container. Check logs with: docker logs sniff-recon-app" -ForegroundColor Red
    exit 1
}
