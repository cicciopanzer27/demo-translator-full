# ================================================
# SETUP TRADUTTORE LAC - Collegamento Desktop
# ================================================
# 
# Questo script:
# 1. Crea collegamento desktop
# 2. Genera icona personalizzata
# 3. Applica icona al collegamento
# 4. Configura avvio silenzioso (senza terminale)
#
# ================================================

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   SETUP TRADUTTORE LAC - Collegamento Desktop" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verifica che siamo nella directory corretta
$CurrentPath = Get-Location
if (-not (Test-Path ".\src\main.py")) {
    Write-Host "ERRORE: Esegui questo script dalla directory TRANSLATOR_LAC!" -ForegroundColor Red
    Write-Host "Directory corrente: $CurrentPath" -ForegroundColor Yellow
    exit 1
}

Write-Host "[1/4] Verifica ambiente..." -ForegroundColor Yellow

# Verifica virtual environment
if (-not (Test-Path ".\venv\Scripts\python.exe")) {
    Write-Host "ERRORE: Virtual environment non trovato!" -ForegroundColor Red
    Write-Host "Esegui prima: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

Write-Host "  OK: Virtual environment trovato" -ForegroundColor Green

Write-Host ""
Write-Host "[2/4] Creazione icona..." -ForegroundColor Yellow

# Installa Pillow se necessario
.\venv\Scripts\pip install Pillow -q

# Crea icona
.\venv\Scripts\python.exe .\scripts\create_icon.py

if (Test-Path ".\scripts\translator_icon.ico") {
    Write-Host "  OK: Icona creata" -ForegroundColor Green
} else {
    Write-Host "  ERRORE: Icona non creata" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[3/4] Creazione collegamento..." -ForegroundColor Yellow

# Crea collegamento
powershell -ExecutionPolicy Bypass -File ".\scripts\create_desktop_shortcut.ps1"

$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Traduttore LAC.lnk"

if (Test-Path $ShortcutPath) {
    Write-Host "  OK: Collegamento creato" -ForegroundColor Green
} else {
    Write-Host "  ERRORE: Collegamento non creato" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[4/4] Applicazione icona..." -ForegroundColor Yellow

# Applica icona
powershell -ExecutionPolicy Bypass -File ".\scripts\update_shortcut_icon.ps1"

Write-Host "  OK: Icona applicata" -ForegroundColor Green

# RIEPILOGO FINALE
Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "   SETUP COMPLETATO CON SUCCESSO!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Collegamento creato sul Desktop:" -ForegroundColor White
Write-Host "  Nome: Traduttore LAC" -ForegroundColor Cyan
Write-Host "  Icona: IT con frecce" -ForegroundColor Cyan
Write-Host ""
Write-Host "Caratteristiche:" -ForegroundColor White
Write-Host "  - Avvio SILENZIOSO (nessun terminale)" -ForegroundColor Green
Write-Host "  - Icona personalizzata" -ForegroundColor Green
Write-Host "  - Italiano centrale" -ForegroundColor Green
Write-Host "  - 7 lingue supportate" -ForegroundColor Green
Write-Host ""
Write-Host "Clicca sull'icona desktop per avviare!" -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

