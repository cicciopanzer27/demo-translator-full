@echo off
echo ==========================================
echo  Traduttore Documenti Legali Offline
echo ==========================================
echo.

REM Attiva virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo ERRORE: Virtual environment non trovato!
    echo Esegui prima: python -m venv venv
    echo               venv\Scripts\activate
    echo               pip install -r requirements.txt
    pause
    exit /b 1
)

REM Avvia applicazione
echo Avvio applicazione...
python src\main.py

REM Se l'applicazione termina con errore
if %ERRORLEVEL% neq 0 (
    echo.
    echo ERRORE durante l'esecuzione!
    echo Controlla i log in logs\translator.log
    pause
)

