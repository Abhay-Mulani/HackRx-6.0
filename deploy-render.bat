@echo off
echo 🚀 Deploying HackRx 6.0 to Render...

REM Check if render-cli is installed
where render >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing Render CLI...
    npm install -g @render-com/render-cli
)

REM Deploy to Render
echo Deploying services...
render deploy

echo ✅ Deployment completed! Check your Render dashboard for status.
pause
