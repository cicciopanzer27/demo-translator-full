@echo off
echo Avvio in modalita' debug...
cd /d "%~dp0"
call venv\Scripts\activate.bat
python src\main.py
echo.
echo Premi un tasto per chiudere...
pause >nul

