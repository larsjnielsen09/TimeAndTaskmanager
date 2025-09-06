@echo off
echo === CURRENT STATUS ===
git status
echo.
echo === FILES THAT WOULD BE ADDED ===
git add -A --dry-run
echo.
echo === TO COMMIT EVERYTHING, RUN ===
echo git add -A
echo git commit -m "Your message here"  
echo git push
