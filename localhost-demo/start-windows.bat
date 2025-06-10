@echo off
echo 🚀 Starting Enterprise AI Consciousness Platform...
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo ✅ Docker is running
echo.

echo 📦 Pulling latest images and starting services...
docker compose pull
docker compose up -d

echo.
echo ⏳ Waiting for services to start (this may take 2-3 minutes)...
timeout /t 30 /nobreak >nul

REM Check if services are running
docker compose ps

echo.
echo 🎉 Deployment complete!
echo.
echo 🌐 Access points:
echo   Main Dashboard: http://localhost:3000
echo   API Documentation: http://localhost:8000/docs
echo   Security Center: http://localhost:3000/security
echo   Analytics: http://localhost:3001
echo.
echo 🔧 Commands:
echo   To view logs: docker compose logs -f
echo   To stop: docker compose down
echo   To restart: docker compose restart
echo.
echo Press any key to continue...
pause >nul