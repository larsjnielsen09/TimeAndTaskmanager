# Simple and Reliable Git Commit Script
# Usage: .\safe-commit.ps1 "Your commit message"

param(
    [Parameter(Mandatory=$true)]
    [string]$Message
)

Write-Host "=== CURRENT STATUS ===" -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "=== ADDING ALL FILES ===" -ForegroundColor Yellow  
git add -A

Write-Host ""
Write-Host "=== FILES TO BE COMMITTED ===" -ForegroundColor Green
git diff --staged --name-only

Write-Host ""
Write-Host "Do you want to commit these files? (y/n): " -ForegroundColor Cyan -NoNewline
$confirm = Read-Host

if ($confirm -eq 'y' -or $confirm -eq 'Y') {
    Write-Host ""
    Write-Host "Committing..." -ForegroundColor Green
    git commit -m $Message
    
    Write-Host ""
    Write-Host "Push to remote? (y/n): " -ForegroundColor Cyan -NoNewline
    $pushConfirm = Read-Host
    
    if ($pushConfirm -eq 'y' -or $pushConfirm -eq 'Y') {
        git push
        Write-Host "Complete!" -ForegroundColor Green
    }
} else {
    Write-Host "Commit cancelled." -ForegroundColor Red
}
