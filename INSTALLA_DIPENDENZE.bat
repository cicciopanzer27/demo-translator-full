@echo off
echo ========================================
echo  INSTALLAZIONE DIPENDENZE
echo ========================================
echo.

cd /d "%~dp0"

echo Installazione dipendenze Python...
venv\Scripts\pip.exe install -r requirements.txt

echo.
echo Installazione modelli traduzione...
venv\Scripts\python.exe -c "import argostranslate.package; argostranslate.package.update_package_index()"

echo.
echo Installazione completata!
echo.
echo Per avviare l'applicazione, esegui: AVVIA_APPLICAZIONE.bat
echo.
pause
