# 🎨 Quick Reference - UI Development on front-end-test

## ⚡ Super Quick Commands

```powershell
# Run the helper script (easiest way!)
.\ui-dev-helper.ps1

# Or use these quick commands:
git status                          # Check what changed
git add .                           # Stage all changes
git commit -m "UI: Your message"    # Commit changes
git push origin front-end-test      # Push to your branch
```

## 🚀 Daily Workflow (3 Steps)

1. **Make UI changes** → Edit CSS/layout in `sniff_recon_gui.py`, `display_packet_table.py`, etc.
2. **Test locally** → `python start_gui.py` or `streamlit run sniff_recon_gui.py`
3. **Commit & Push** → `git add .` → `git commit -m "UI: description"` → `git push origin front-end-test`

## ⚠️ Golden Rules

1. ✅ **ALWAYS** work on `front-end-test` branch
2. ❌ **NEVER** push to `main` branch
3. ✅ **ALWAYS** test changes locally before pushing
4. ✅ **SYNC** with main branch regularly: `git merge origin/main`
5. ✅ **CREATE PR** when feature is complete for review by @mfscpayload-690

## 📁 Files You'll Edit

| File | What It Does |
|------|-------------|
| `sniff_recon_gui.py` | Main UI, CSS, file uploader, tabs |
| `display_packet_table.py` | Packet table styling, protocol cards |
| `ai_query_interface.py` | AI chat interface styling |

## 🎨 Current Color Scheme

```
Primary:    #00ffff (Cyan)
Secondary:  #00b3b3 (Dark Cyan)  
Background: #0f0f23 → #1a1a2e (Gradient)
Text:       #e0e0e0 (Light Gray)
```

## 🆘 Emergency Commands

```powershell
# Undo changes (before commit)
git checkout -- filename.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Check which branch you're on
git branch --show-current

# Switch to front-end-test
git checkout front-end-test

# Discard ALL local changes
git reset --hard HEAD
```

## 📋 Pull Request Checklist

When ready to merge your UI work:

- [ ] All changes committed and pushed to `front-end-test`
- [ ] Synced with latest `main` branch
- [ ] Tested locally with sample files
- [ ] No console errors (F12 in browser)
- [ ] Screenshots of changes ready
- [ ] Created PR on GitHub targeting `main` from `front-end-test`
- [ ] Tagged @mfscpayload-690 as reviewer

---

**Your Info**:  
👤 Developer: krizzdev7 (Devu Krishna)  
🌿 Branch: front-end-test  
📧 Email: dev777kris@gmail.com  
🏢 Repo: mfscpayload-690/Sniff-Recon

**Need Help?** Read `UI_DEVELOPMENT_WORKFLOW.md` for detailed guide!
