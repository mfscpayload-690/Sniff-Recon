# Sniff Recon - Docker Deployment Note

## Important: Docker-Only Deployment

As of November 7, 2025, Sniff Recon runs **exclusively in Docker containers** for production use.

### Why Docker-Only?

1. **Consistency**: Same environment across all machines
2. **Isolation**: No conflicts with system Python packages
3. **Security**: Containerized security boundaries
4. **Easy Deployment**: One command to start/stop
5. **Health Monitoring**: Built-in health checks

### How to Use

**Start Sniff Recon:**
```powershell
# Windows
.\docker-start.ps1

# Or use docker-compose directly
docker-compose up -d
```

**Stop Sniff Recon:**
```powershell
# Windows
.\docker-stop.ps1

# Or use docker-compose directly
docker-compose down
```

**View Logs:**
```powershell
docker logs sniff-recon-app -f
```

**Access the Application:**
- Open your browser and navigate to: http://localhost:8501

### Local Development

Local installation (without Docker) is only supported for development purposes:
- Testing new features
- Debugging code changes
- Development iterations

For any production use, testing, or deployment, **always use Docker**.

### Files

- `Dockerfile` - Container image definition
- `docker-compose.yml` - Service orchestration
- `docker-start.ps1` - Windows start script
- `docker-stop.ps1` - Windows stop script
- `.dockerignore` - Files excluded from build

### Troubleshooting

**Container won't start:**
```powershell
docker logs sniff-recon-app
```

**Port already in use:**
```powershell
# Check what's using port 8501
netstat -ano | findstr ":8501"

# Kill the process
Stop-Process -Id <PID> -Force
```

**Need to rebuild:**
```powershell
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```
