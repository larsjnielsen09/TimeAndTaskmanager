# Reliable Git Commit Script
# Usage: .\commit.ps1 "Your commit message"

param(
    [Parameter(Mandatory=$true)]
    [string]$Message
)

Write-Host "Checking repository status..." -ForegroundColor Yellow
git status

Write-Host "`nAdding ALL files (including new ones)..." -ForegroundColor Yellow  
git add -A

Write-Host "`nFiles that will be committed:" -ForegroundColor Green
git diff --staged --name-only

Write-Host "`nDo you want to commit these files? (y/n): " -ForegroundColor Cyan -NoNewline
$confirm = Read-Host

if ($confirm -eq 'y' -or $confirm -eq 'Y') {
    Write-Host "`nCommitting..." -ForegroundColor Green
    git commit -m $Message
    
    Write-Host "`nPush to remote? (y/n): " -ForegroundColor Cyan -NoNewline
    $pushConfirm = Read-Host
    
    if ($pushConfirm -eq 'y' -or $pushConfirm -eq 'Y') {
        git push
        Write-Host "All done!" -ForegroundColor Green
    }
} else {
    Write-Host "Commit cancelled." -ForegroundColor Red
}
