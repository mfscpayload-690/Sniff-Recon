# UI Development Workflow for Sniff Recon
**Developer**: krizzdev7 (Devu Krishna)  
**Branch**: `front-end-test`  
**Main Repository**: mfscpayload-690/Sniff-Recon

---

## 🎯 Your Current Setup

You are now working on the `front-end-test` branch. All your UI changes will be isolated from the main branch until they're reviewed and merged via Pull Request.

```
✅ Current Branch: front-end-test
✅ Git User: Devu Krishna (dev777kris@gmail.com)
✅ Remote: origin (mfscpayload-690/Sniff-Recon)
```

---

## 📋 Daily Workflow

### 1. Start Your Work Session
```powershell
# Always ensure you're on the correct branch
git checkout front-end-test

# Pull latest changes from the branch
git pull origin front-end-test

# If main branch has updates you need, sync them:
git fetch origin main
git merge origin/main  # Merge main into your branch
```

### 2. Make Your UI Changes
Work on any of these UI files:
- `sniff_recon_gui.py` - Main GUI layout and styling
- `display_packet_table.py` - Packet table UI components
- `ai_query_interface.py` - AI chat interface
- CSS in any `inject_*_css()` functions

### 3. Test Your Changes Locally
```powershell
# Option 1: Run with Python
python start_gui.py

# Option 2: Run with Streamlit directly
streamlit run sniff_recon_gui.py

# Option 3: Test in Docker
docker-compose up --build
```

### 4. Commit Your Changes
```powershell
# Check what files you changed
git status

# Stage your changes
git add .

# Commit with descriptive message
git commit -m "UI: Description of your changes"

# Examples:
# git commit -m "UI: Redesigned packet table with modern card layout"
# git commit -m "UI: Updated color scheme for cyberpunk theme"
# git commit -m "UI: Added responsive design for mobile devices"
```

### 5. Push to Your Branch
```powershell
# Push to front-end-test branch
git push origin front-end-test
```

**🚨 IMPORTANT**: Never push to `main` branch! Always push to `front-end-test`.

---

## 🔄 Creating a Pull Request (When Ready)

When you've completed a feature or set of UI improvements and want them reviewed:

### Step 1: Ensure Your Branch is Up-to-Date
```powershell
# Fetch latest changes
git fetch origin

# Merge main branch changes into your branch (if any)
git merge origin/main

# Resolve any conflicts if they occur
# Then push updated branch
git push origin front-end-test
```

### Step 2: Create Pull Request on GitHub
1. Go to: https://github.com/mfscpayload-690/Sniff-Recon
2. Click on **"Pull requests"** tab
3. Click **"New pull request"**
4. Set:
   - **Base**: `main` (where changes will go)
   - **Compare**: `front-end-test` (your branch)
5. Click **"Create pull request"**
6. Fill in the PR template:

```markdown
## UI Improvements

### Changes Made
- [List your UI changes here]
- Updated color scheme
- Redesigned packet table layout
- Added responsive design

### Screenshots
[Attach before/after screenshots]

### Testing Done
- [x] Tested locally with `streamlit run`
- [x] Tested in Docker container
- [x] Verified on Chrome/Firefox/Edge
- [x] Tested with sample PCAP files

### Breaking Changes
- [ ] None
- [ ] Yes (describe below)

### Additional Notes
Any special notes for the reviewer (mfscpayload-690)

---
**UI Developer**: @krizzdev7
**Reviewer**: @mfscpayload-690
```

### Step 3: Request Review
- Tag `@mfscpayload-690` as reviewer
- Add labels: `enhancement`, `UI/UX`, `front-end`
- Wait for review and feedback

---

## 🛠️ Quick Commands Reference

### Branch Management
```powershell
# Check current branch
git branch --show-current

# Switch to front-end-test
git checkout front-end-test

# See all branches
git branch -a

# See commit history
git log --oneline -10
```

### Syncing with Main Branch
```powershell
# Get latest from main without switching branches
git fetch origin main

# Merge main into your current branch (front-end-test)
git merge origin/main

# If conflicts occur:
# 1. Git will mark conflicted files
# 2. Open files and resolve conflicts (look for <<<<<<< markers)
# 3. After resolving:
git add .
git commit -m "Merge main branch into front-end-test"
git push origin front-end-test
```

### Undo Changes (Before Commit)
```powershell
# Discard changes to specific file
git checkout -- filename.py

# Discard all changes
git reset --hard HEAD
```

### Undo Last Commit (After Commit, Before Push)
```powershell
# Undo commit but keep changes
git reset --soft HEAD~1

# Undo commit and discard changes
git reset --hard HEAD~1
```

---

## 🎨 UI Development Guidelines

### Files You'll Primarily Work On

1. **`sniff_recon_gui.py`** (Lines 26-220)
   - Main CSS injection function `inject_modern_css()`
   - Global styles, color schemes, animations
   - File uploader styling
   - Tab styling

2. **`display_packet_table.py`** (Lines 10-100)
   - Packet table CSS
   - Protocol card styling
   - Interactive elements

3. **`ai_query_interface.py`** (Lines 10-100)
   - AI chat interface CSS
   - Query input styling
   - Response containers

### Design System (Current Theme)
```css
Primary Color: #00ffff (Cyan)
Secondary Color: #00b3b3 (Dark Cyan)
Background: linear-gradient(135deg, #0f0f23, #1a1a2e, #16213e)
Text Color: #e0e0e0 (Light Gray)
Card Background: rgba(30, 30, 30, 0.8)
Border: rgba(0, 255, 255, 0.3)
Font: 'Inter', sans-serif
```

### Testing Checklist
- [ ] Test with small PCAP files (<1MB)
- [ ] Test with large PCAP files (50-100MB)
- [ ] Test CSV file upload
- [ ] Test AI query interface
- [ ] Test all tabs (Packet Analysis, AI Analysis, Export)
- [ ] Test responsive design (resize browser)
- [ ] Check console for errors (F12 in browser)

---

## 🐳 Docker Development

If you want to test in Docker (recommended for production-like environment):

```powershell
# Build and run
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop container
docker-compose down

# Rebuild after UI changes
docker-compose up --build -d
```

---

## 🚨 Common Issues & Solutions

### Issue: "Your branch is behind origin/front-end-test"
**Solution**:
```powershell
git pull origin front-end-test
```

### Issue: "Merge conflict in filename.py"
**Solution**:
1. Open the file in VS Code
2. Look for conflict markers: `<<<<<<<`, `=======`, `>>>>>>>`
3. Choose which changes to keep
4. Remove conflict markers
5. `git add .` → `git commit` → `git push`

### Issue: "Permission denied (publickey)"
**Solution**:
```powershell
# Make sure you're authenticated with GitHub
# Use GitHub Desktop or set up SSH keys
# Or use HTTPS with Personal Access Token
```

### Issue: Accidentally committed to main branch
**Solution**:
```powershell
# STOP! Do not push!
git checkout front-end-test
git cherry-pick <commit-hash>  # Copy commit to correct branch
git push origin front-end-test

# Then reset main branch
git checkout main
git reset --hard origin/main
```

---

## 📝 Commit Message Conventions

Use clear, descriptive commit messages prefixed with type:

```
UI: [Your change description]
FIX: [Bug fix description]
STYLE: [Style/CSS only changes]
REFACTOR: [Code restructuring]
DOCS: [Documentation updates]

Examples:
✅ UI: Redesigned packet table with card-based layout
✅ STYLE: Updated cyberpunk color scheme for better contrast
✅ FIX: Resolved responsive design issue on mobile devices
✅ REFACTOR: Extracted CSS into separate inject function
```

---

## 🎯 Current Project Status

**Your Role**: UI/UX Developer (Front-end)  
**Your Branch**: `front-end-test`  
**Main Developer**: mfscpayload-690 (Backend/Core Logic)

**Workflow**:
1. You develop UI improvements on `front-end-test`
2. When ready, create Pull Request
3. mfscpayload-690 reviews your PR
4. After approval, changes are merged to `main`
5. You continue with next UI feature

---

## 📞 Need Help?

- **Branch Issues**: Check this guide first
- **UI Design Questions**: Refer to `copilot-instructions.md` for patterns
- **Merge Conflicts**: Ask main dev (mfscpayload-690) before force-pushing
- **Testing Issues**: Check `docs/TROUBLESHOOTING.md`

---

**Last Updated**: November 6, 2025  
**Your Branch**: front-end-test  
**Status**: ✅ Ready for UI Development
