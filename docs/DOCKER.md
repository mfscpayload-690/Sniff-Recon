# 🐳 Docker Deployment Guide for Sniff Recon

## Prerequisites

- **Docker Desktop** installed on Windows
  - Download from: https://www.docker.com/products/docker-desktop/
- **Docker Compose** (included with Docker Desktop)

## Quick Start

### 1. Build and Run with Docker Compose

```powershell
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

The app will be available at **http://localhost:8501**

### 2. Using Docker CLI Directly

```powershell
# Build the image
docker build -t sniff-recon:latest .

# Run the container
docker run -d `
  --name sniff-recon `
  -p 8501:8501 `
  -v ${PWD}/output:/app/output `
  -v ${PWD}/.env:/app/.env:ro `
  sniff-recon:latest

# View logs
docker logs -f sniff-recon

# Stop and remove
docker stop sniff-recon
docker rm sniff-recon
```

## Environment Setup

Make sure your `.env` file exists with your API keys:

```env
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## Docker Commands Cheat Sheet

### Container Management

```powershell
# Start container
docker-compose up -d

# Stop container
docker-compose down

# Restart container
docker-compose restart

# View running containers
docker ps

# View all containers (including stopped)
docker ps -a
```

### Logs and Debugging

```powershell
# View logs
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100

# Execute command in running container
docker-compose exec sniff-recon bash

# Check container health
docker inspect sniff-recon | findstr Health
```

### Cleanup

```powershell
# Remove stopped containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Remove image
docker rmi sniff-recon:latest

# Clean up all unused Docker resources
docker system prune -a
```

## Updating the Application

```powershell
# Pull latest code changes
git pull

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

## Troubleshooting

### Port Already in Use

If port 8501 is already in use, edit `docker-compose.yml`:

```yaml
ports:
  - "8502:8501"  # Use port 8502 instead
```

### Container Won't Start

```powershell
# Check logs
docker-compose logs

# Check if port is in use
netstat -ano | findstr :8501

# Force recreate
docker-compose up -d --force-recreate
```

### API Keys Not Working

```powershell
# Verify .env file is mounted
docker-compose exec sniff-recon cat /app/.env

# Restart container after .env changes
docker-compose restart
```

## Production Deployment

### Using Docker Hub

```powershell
# Tag image
docker tag sniff-recon:latest yourusername/sniff-recon:latest

# Push to Docker Hub
docker push yourusername/sniff-recon:latest

# Pull and run on another machine
docker pull yourusername/sniff-recon:latest
docker-compose up -d
```

### Using Docker Swarm (Optional)

```powershell
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml sniff-recon

# List services
docker service ls

# Remove stack
docker stack rm sniff-recon
```

## Benefits of Docker Deployment

✅ **Consistent Environment** - Same Python version (3.11) everywhere  
✅ **No Dependency Conflicts** - Isolated from your system Python  
✅ **Easy Deployment** - One command to start everything  
✅ **Portability** - Run on Windows, Linux, macOS, or cloud  
✅ **Quick Updates** - Rebuild and restart in seconds  
✅ **Resource Management** - Docker handles resource limits  

## Next Steps

1. **Test locally** with `docker-compose up -d`
2. **Deploy to cloud** (AWS, Azure, Google Cloud, Heroku)
3. **Set up CI/CD** for automatic deployments
4. **Monitor with** Docker stats or Portainer

## Support

For issues:
- Check logs: `docker-compose logs -f`
- Verify .env file exists and has valid API keys
- Ensure Docker Desktop is running
- Check port 8501 is not in use
