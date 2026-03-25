@echo off
echo ============================================
echo  Travel Genie AI - Frontend Server
echo ============================================
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing npm dependencies...
    npm install
)

echo.
echo Starting Frontend on http://localhost:5173
echo (Press Ctrl+C to stop)
echo.
npm run dev
