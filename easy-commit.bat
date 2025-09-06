@echo off
echo.
echo === CURRENT STATUS ===
git status
echo.
echo === ADDING ALL FILES ===
git add -A
echo.
echo === FILES TO BE COMMITTED ===
git diff --staged --name-only
echo.
set /p confirm="Do you want to commit these files? (y/n): "
if /i "%confirm%"=="y" (
    set /p message="Enter commit message: "
    git commit -m "%message%"
    echo.
    set /p push="Push to remote? (y/n): "
    if /i "%push%"=="y" (
        git push
        echo Complete!
    )
) else (
    echo Commit cancelled.
)
