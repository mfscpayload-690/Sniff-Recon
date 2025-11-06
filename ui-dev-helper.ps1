# UI Development Helper Script for Sniff Recon
# Quick commands for common Git operations on front-end-test branch

Write-Host "🎨 Sniff Recon UI Development Helper" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check current branch
$currentBranch = git branch --show-current
if ($currentBranch -ne "front-end-test") {
    Write-Host "⚠️  WARNING: You're on '$currentBranch' branch, not 'front-end-test'!" -ForegroundColor Yellow
    Write-Host "Switching to front-end-test branch..." -ForegroundColor Yellow
    git checkout front-end-test
    Write-Host "✅ Switched to front-end-test" -ForegroundColor Green
} else {
    Write-Host "✅ You're on the correct branch: front-end-test" -ForegroundColor Green
}

Write-Host ""
Write-Host "Choose an action:" -ForegroundColor Cyan
Write-Host "1. 📥 Pull latest changes from front-end-test"
Write-Host "2. 🔄 Sync with main branch (merge main into front-end-test)"
Write-Host "3. 💾 Commit and push changes"
Write-Host "4. 📊 View status and recent commits"
Write-Host "5. 🚀 Run app locally (Streamlit)"
Write-Host "6. 🐳 Run app in Docker"
Write-Host "7. 🔍 View diff of changes"
Write-Host "8. 📝 Create Pull Request guide"
Write-Host "9. ❌ Exit"
Write-Host ""

$choice = Read-Host "Enter your choice (1-9)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "📥 Pulling latest changes from front-end-test..." -ForegroundColor Cyan
        git pull origin front-end-test
        Write-Host ""
        Write-Host "✅ Done!" -ForegroundColor Green
    }
    "2" {
        Write-Host ""
        Write-Host "🔄 Syncing with main branch..." -ForegroundColor Cyan
        Write-Host "Fetching latest main branch..." -ForegroundColor Yellow
        git fetch origin main
        Write-Host "Merging main into front-end-test..." -ForegroundColor Yellow
        git merge origin/main
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✅ Successfully merged main into front-end-test!" -ForegroundColor Green
            Write-Host "Don't forget to push: git push origin front-end-test" -ForegroundColor Yellow
        } else {
            Write-Host ""
            Write-Host "⚠️  Merge conflicts detected! Please resolve them manually." -ForegroundColor Red
            Write-Host "1. Open conflicted files in VS Code" -ForegroundColor Yellow
            Write-Host "2. Resolve conflicts (look for <<<<<<< markers)" -ForegroundColor Yellow
            Write-Host "3. Run: git add ." -ForegroundColor Yellow
            Write-Host "4. Run: git commit -m 'Merge main into front-end-test'" -ForegroundColor Yellow
            Write-Host "5. Run: git push origin front-end-test" -ForegroundColor Yellow
        }
    }
    "3" {
        Write-Host ""
        git status
        Write-Host ""
        $hasChanges = git status --porcelain
        if ([string]::IsNullOrEmpty($hasChanges)) {
            Write-Host "ℹ️  No changes to commit." -ForegroundColor Yellow
        } else {
            Write-Host "💾 Committing changes..." -ForegroundColor Cyan
            Write-Host ""
            $commitMsg = Read-Host "Enter commit message (e.g., 'UI: Updated color scheme')"
            
            if ([string]::IsNullOrEmpty($commitMsg)) {
                Write-Host "❌ Commit message cannot be empty!" -ForegroundColor Red
            } else {
                git add .
                git commit -m "$commitMsg"
                
                Write-Host ""
                $pushChoice = Read-Host "Push to origin/front-end-test? (y/n)"
                if ($pushChoice -eq "y" -or $pushChoice -eq "Y") {
                    Write-Host "🚀 Pushing to front-end-test..." -ForegroundColor Cyan
                    git push origin front-end-test
                    Write-Host ""
                    Write-Host "✅ Changes pushed successfully!" -ForegroundColor Green
                } else {
                    Write-Host "ℹ️  Changes committed locally. Push later with: git push origin front-end-test" -ForegroundColor Yellow
                }
            }
        }
    }
    "4" {
        Write-Host ""
        Write-Host "📊 Current Status:" -ForegroundColor Cyan
        Write-Host "==================" -ForegroundColor Cyan
        git status
        Write-Host ""
        Write-Host "📜 Recent Commits:" -ForegroundColor Cyan
        Write-Host "==================" -ForegroundColor Cyan
        git log --oneline -10 --graph --decorate
    }
    "5" {
        Write-Host ""
        Write-Host "🚀 Starting Sniff Recon locally..." -ForegroundColor Cyan
        Write-Host "App will open at http://localhost:8501" -ForegroundColor Yellow
        Write-Host "Press Ctrl+C in terminal to stop" -ForegroundColor Yellow
        Write-Host ""
        python start_gui.py
    }
    "6" {
        Write-Host ""
        Write-Host "🐳 Starting Sniff Recon in Docker..." -ForegroundColor Cyan
        Write-Host "Building and starting container..." -ForegroundColor Yellow
        docker-compose up --build -d
        Write-Host ""
        Write-Host "✅ Container started!" -ForegroundColor Green
        Write-Host "📱 App URL: http://localhost:8501" -ForegroundColor Cyan
        Write-Host "📋 View logs: docker-compose logs -f" -ForegroundColor Yellow
        Write-Host "⏹️  Stop container: docker-compose down" -ForegroundColor Yellow
        
        Start-Sleep -Seconds 2
        Start-Process "http://localhost:8501"
    }
    "7" {
        Write-Host ""
        Write-Host "🔍 Viewing changes..." -ForegroundColor Cyan
        git diff
    }
    "8" {
        Write-Host ""
        Write-Host "📝 Creating Pull Request Guide" -ForegroundColor Cyan
        Write-Host "==============================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "1. Ensure your branch is up-to-date:" -ForegroundColor Yellow
        Write-Host "   git fetch origin" -ForegroundColor White
        Write-Host "   git merge origin/main" -ForegroundColor White
        Write-Host "   git push origin front-end-test" -ForegroundColor White
        Write-Host ""
        Write-Host "2. Go to GitHub:" -ForegroundColor Yellow
        Write-Host "   https://github.com/mfscpayload-690/Sniff-Recon/pulls" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "3. Click 'New pull request'" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "4. Set branches:" -ForegroundColor Yellow
        Write-Host "   Base: main" -ForegroundColor White
        Write-Host "   Compare: front-end-test" -ForegroundColor White
        Write-Host ""
        Write-Host "5. Fill in PR details:" -ForegroundColor Yellow
        Write-Host "   - Title: UI: [Brief description]" -ForegroundColor White
        Write-Host "   - Description: List your changes" -ForegroundColor White
        Write-Host "   - Screenshots: Attach before/after images" -ForegroundColor White
        Write-Host "   - Reviewer: @mfscpayload-690" -ForegroundColor White
        Write-Host ""
        Write-Host "6. Create PR and wait for review!" -ForegroundColor Green
        Write-Host ""
        
        $openGH = Read-Host "Open GitHub Pull Requests page? (y/n)"
        if ($openGH -eq "y" -or $openGH -eq "Y") {
            Start-Process "https://github.com/mfscpayload-690/Sniff-Recon/pulls"
        }
    }
    "9" {
        Write-Host ""
        Write-Host "👋 Happy coding!" -ForegroundColor Green
        exit
    }
    default {
        Write-Host ""
        Write-Host "❌ Invalid choice. Please run the script again." -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
