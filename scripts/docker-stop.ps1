# Sniff Recon - Docker Stop Script
# This script stops and removes Sniff Recon Docker containers

Write-Host "🛑 Stopping Sniff Recon Docker container..." -ForegroundColor Yellow

docker-compose down

Write-Host "✅ Sniff Recon stopped successfully!" -ForegroundColor Green
