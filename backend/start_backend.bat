@echo off
echo ============================================
echo  Travel Genie AI - Backend Server
echo ============================================
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting Backend Server on http://localhost:8000
echo (Press Ctrl+C to stop)
echo.
python main.py
