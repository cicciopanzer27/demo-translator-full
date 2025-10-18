@echo off
echo ================================================
echo CREAZIONE ICONA DESKTOP - TRADUTTORE DOCUMENTI
echo ================================================
echo.

REM Crea icona sul desktop
powershell -ExecutionPolicy Bypass -File "scripts\create_desktop_shortcut.ps1"

echo.
echo [OK] Icona creata sul desktop!
echo.
echo Puoi ora avviare il traduttore cliccando sull'icona.
echo.
pause
