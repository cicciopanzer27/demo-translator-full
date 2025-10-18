@echo off
echo ========================================
echo  TRADUTTORE DOCUMENTI LEGALI OFFLINE
echo ========================================
echo.
echo Avvio applicazione...
echo.

cd /d "%~dp0"
venv\Scripts\python.exe src\main.py

echo.
echo Applicazione chiusa.
pause
