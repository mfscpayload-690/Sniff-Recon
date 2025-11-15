# 🐳 Docker Development Guide - Sniff Recon UI

**Developer**: krizzdev7 | **Branch**: front-end-test | **This is a DOCKER-FIRST project!**

---

## 🚀 Quick Start (3 Commands)

```powershell
# 1. Make your UI changes in code
# 2. Rebuild and run
docker-compose up --build -d

# 3. Open browser
# App: http://localhost:8501
```

---

## 🐳 Why Docker-First?

- ✅ **Matches production environment exactly**
- ✅ **No "works on my machine" issues**
- ✅ **Consistent dependencies across all developers**
- ✅ **Easy deployment** - same container in dev and prod
- ✅ **Isolated environment** - doesn't mess with your system Python

---

## 📋 Complete Docker Workflow

### 1️⃣ Make Your UI Changes
Edit any of these files:
- `src/ui/gui.py` - Main UI and CSS
- `src/ui/display_packet_table.py` - Packet table styling
- `src/ui/ui_packet_viewer.py` - Packet inspection interface

### 2️⃣ Test in Docker
```powershell
# ALWAYS rebuild after making changes!
docker-compose up --build -d

# Wait 10-15 seconds for container to start
# Then open: http://localhost:8501
```

### 3️⃣ Check Logs (If Issues)
```powershell
# View real-time logs
docker-compose logs -f

# View last 50 lines
docker-compose logs --tail=50

# Check container status
docker ps
```

### 4️⃣ Iterate on Changes
```powershell
# Stop container
docker-compose down

# Make more changes to code
# ...

# Rebuild and test again
docker-compose up --build -d
```

### 5️⃣ Commit & Push to front-end-test
```powershell
git add .
git commit -m "UI: Description of changes"
git push origin front-end-test  # ⚠️ ALWAYS front-end-test!
```

---

## 🛠️ Essential Docker Commands

### Starting & Stopping
```powershell
# Build and start (use after code changes)
docker-compose up --build -d

# Start without rebuilding (use if no code changes)
docker-compose up -d

# Stop and remove container
docker-compose down

# Restart without rebuilding
docker-compose restart
```

### Debugging & Logs
```powershell
# View logs in real-time
docker-compose logs -f

# View last N lines
docker-compose logs --tail=100

# Check if container is running
docker ps

# Check all containers (including stopped)
docker ps -a

# Execute command inside container
docker-compose exec sniff-recon bash

# Check container health
docker inspect sniff-recon-app --format='{{json .State.Health}}'
```

### Cleanup
```powershell
# Remove stopped containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Remove all unused Docker resources
docker system prune -a
```

---

## 🔍 Testing Your UI Changes

### Before Committing, Test:

1. **Upload Test Files**
   - Small PCAP (< 1MB)
   - Large PCAP (50-100MB)
   - CSV file
   - Invalid file (should show error gracefully)

2. **Check All Tabs**
   - 📊 Packet Analysis tab
   - 🤖 AI Analysis tab
   - 💾 Export Results tab

3. **Test Responsive Design**
   - Resize browser window
   - Check mobile view (F12 → Device toolbar)

4. **Check Console for Errors**
   - Press F12 in browser
   - Look for red errors in Console tab
   - Fix any CSS or JavaScript errors

5. **Verify in Docker Logs**
   ```powershell
   docker-compose logs --tail=100
   ```
   - No Python errors
   - Streamlit started successfully
   - No dependency issues

---

## 🎨 Typical UI Development Session

```powershell
# Morning: Pull latest changes
git checkout front-end-test
git pull origin front-end-test

# Start Docker container
docker-compose up --build -d

# Open in browser
# http://localhost:8501

# === DEVELOPMENT LOOP ===
# 1. Make CSS/UI changes in VS Code
# 2. Save files
# 3. Rebuild Docker: docker-compose up --build -d
# 4. Refresh browser to see changes
# 5. Repeat until satisfied

# Stop container when done
docker-compose down

# Commit changes
git add .
git commit -m "UI: Redesigned packet table layout"
git push origin front-end-test
```

---

## 🐛 Troubleshooting Docker Issues

### Container Won't Start
```powershell
# Check logs
docker-compose logs

# Remove old containers and rebuild
docker-compose down
docker-compose up --build -d
```

### Port 8501 Already in Use
```powershell
# Stop any existing Streamlit processes
Get-Process -Name streamlit -ErrorAction SilentlyContinue | Stop-Process -Force

# Or change port in docker-compose.yml:
# ports:
#   - "8502:8501"
```

### Changes Not Showing Up
```powershell
# Force rebuild without cache
docker-compose build --no-cache
docker-compose up -d

# Clear browser cache (Ctrl+Shift+R)
```

### Container Shows "unhealthy"
```powershell
# This is normal! Health check needs curl installed
# App still works fine. Verify by opening http://localhost:8501

# Optional: Install curl in container
docker-compose exec sniff-recon bash -c "apt-get update && apt-get install -y curl"
```

### Out of Disk Space
```powershell
# Clean up unused Docker resources
docker system prune -a

# Remove old images
docker image prune -a
```

---

## 📦 Docker Files in Project

- **`Dockerfile`** - Container build instructions (DON'T EDIT unless you know what you're doing)
- **`docker-compose.yml`** - Container configuration (ports, volumes, env vars)
- **`.dockerignore`** - Files excluded from Docker build
- **`.env`** - Environment variables (API keys) - mounted into container

---

## 🔐 Environment Variables in Docker

Your `.env` file is automatically mounted into the container:
```yaml
# In docker-compose.yml:
volumes:
  - ./.env:/app/.env:ro  # Read-only mount
```

So your API keys work in Docker automatically! 🎉

---

## 🎯 Git + Docker Workflow Summary

```powershell
# 1. Switch to front-end-test branch
git checkout front-end-test

# 2. Pull latest changes
git pull origin front-end-test

# 3. Make UI changes in code editor

# 4. Test in Docker
docker-compose up --build -d

# 5. Verify at http://localhost:8501

# 6. Stop container
docker-compose down

# 7. Commit changes
git add .
git commit -m "UI: Your changes"

# 8. Push to front-end-test (NEVER main!)
git push origin front-end-test

# 9. When feature complete, create PR on GitHub
```

---

## ⚠️ CRITICAL REMINDERS

1. 🐳 **ALWAYS test in Docker** - `docker-compose up --build -d`
2. 🌿 **ALWAYS push to front-end-test** - Never to main!
3. 🔄 **ALWAYS rebuild** after code changes - `--build` flag is important!
4. 📱 **ALWAYS test UI** at http://localhost:8501 before committing
5. 🧹 **ALWAYS stop containers** when done - `docker-compose down`

---

## 🆘 Quick Help

```powershell
# Is container running?
docker ps | Select-String "sniff-recon"

# What's my current branch?
git branch --show-current

# Kill everything and start fresh
docker-compose down -v
docker system prune -a
git checkout front-end-test
docker-compose up --build -d
```

---

**Remember**: Docker is your production environment! If it works in Docker, it'll work in production! 🚀
