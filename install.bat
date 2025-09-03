@echo off
echo 🚀 Installing DeepRecon dependencies on Windows...

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.x and rerun this script.
    pause
    exit /b
)

:: Install requirements
pip install -r requirements.txt

:: Tor installation note
echo 🔍 Please download Tor Expert Bundle from:
echo https://www.torproject.org/download/tor/
echo Extract and run: tor.exe

echo ✅ Installation complete!
echo Run the tool with: python main.py
pause
