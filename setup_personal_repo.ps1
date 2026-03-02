# PowerShell script to set up repository for personal GitHub push
# Usage: .\setup_personal_repo.ps1 -GitHubUsername "yourusername" -RepoName "your-repo-name" -FreshStart

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername,
    
    [Parameter(Mandatory=$true)]
    [string]$RepoName,
    
    [switch]$FreshStart
)

$repoUrl = "https://github.com/$GitHubUsername/$RepoName.git"

Write-Host "Setting up repository for personal GitHub push..." -ForegroundColor Green
Write-Host "Repository URL: $repoUrl" -ForegroundColor Cyan

# Check if .git directory exists
if (Test-Path .git) {
    Write-Host "Git repository detected." -ForegroundColor Yellow
    
    if ($FreshStart) {
        Write-Host "Starting fresh (removing git history)..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force .git
        Write-Host "Git history removed." -ForegroundColor Green
        
        Write-Host "Initializing new git repository..." -ForegroundColor Yellow
        git init
        git branch -M main
        
        Write-Host "Adding all files..." -ForegroundColor Yellow
        git add .
        
        Write-Host "Creating initial commit..." -ForegroundColor Yellow
        git commit -m "Initial commit"
    } else {
        Write-Host "Removing existing remotes..." -ForegroundColor Yellow
        $remotes = git remote
        foreach ($remote in $remotes) {
            git remote remove $remote
            Write-Host "Removed remote: $remote" -ForegroundColor Green
        }
    }
} else {
    Write-Host "No git repository found. Initializing new one..." -ForegroundColor Yellow
    git init
    git branch -M main
    git add .
    git commit -m "Initial commit"
}

# Add new remote
Write-Host "Adding new remote: origin -> $repoUrl" -ForegroundColor Yellow
git remote add origin $repoUrl

Write-Host "`nSetup complete! Next steps:" -ForegroundColor Green
Write-Host "1. Make sure the repository '$RepoName' exists on GitHub" -ForegroundColor Cyan
Write-Host "2. Run: git push -u origin main" -ForegroundColor Cyan
if ($FreshStart) {
    Write-Host "   (or use --force if the remote repository already exists)" -ForegroundColor Yellow
}

Write-Host "`nTo push now, run:" -ForegroundColor Green
Write-Host "   git push -u origin main" -ForegroundColor White
