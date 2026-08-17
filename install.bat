@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo   🕵️‍♂️ DeepRecon - OSINT Framework Setup
echo ===================================================
echo.
echo Installing DeepRecon dependencies on Windows...

where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python launcher not found. Install Python 3.10+ first.
    pause
    exit /b 1
)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo ---------------------------------------------------
echo  [IMPORTANT] Tor Network Configuration
echo ---------------------------------------------------
echo  Download the Tor Expert Bundle or Tor Browser:
echo  https://www.torproject.org/download/tor/
echo  Ensure tor.exe is running on port 9050 before crawling.
echo ---------------------------------------------------
echo.

echo Creating deeprecon.bat CLI launcher...
(
echo @echo off
echo python "%%~dp0main.py" %%*
) > "%~dp0deeprecon.bat"

echo.
echo [SUCCESS] DeepRecon setup complete!
echo Launch options:
echo   1. Interactive CLI: deeprecon --cli   (or python main.py)
echo   2. Web Dashboard:   deeprecon --web   (or python main.py --web)
echo.
pause
