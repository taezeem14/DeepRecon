@echo off
setlocal enabledelayedexpansion

echo Installing DeepRecon dependencies on Windows...

where py >nul 2>&1
if errorlevel 1 (
    echo Python launcher not found. Install Python 3.x first.
    pause
    exit /b 1
)

py -3 -m pip install --upgrade pip
py -3 -m pip install -r requirements.txt

echo.
echo Install the Tor Expert Bundle separately:
echo https://www.torproject.org/download/tor/
echo Then run tor.exe before starting DeepRecon.
echo.

echo Creating deeprecon.bat wrapper...
(
echo @echo off
echo py -3 "%~dp0main.py" %%*
) > deeprecon.bat

echo Installation complete.
echo You can run the tool by calling: deeprecon --cli OR deeprecon --web
echo (Make sure this directory is in your PATH to call it from anywhere)
pause
