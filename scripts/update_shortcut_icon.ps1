# Script per aggiornare l'icona del collegamento desktop

$WshShell = New-Object -ComObject WScript.Shell

# Percorsi
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Traduttore LAC.lnk"
$ProjectPath = "C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC"
$IconPath = Join-Path $ProjectPath "scripts\translator_icon.ico"

# Verifica che il collegamento esista
if (-not (Test-Path $ShortcutPath)) {
    Write-Host "Errore: Collegamento non trovato!"
    Write-Host "Esegui prima: .\scripts\create_desktop_shortcut.ps1"
    exit 1
}

# Verifica che l'icona esista
if (-not (Test-Path $IconPath)) {
    Write-Host "Errore: Icona non trovata!"
    Write-Host "Esegui prima: .\venv\Scripts\python.exe .\scripts\create_icon.py"
    exit 1
}

# Aggiorna collegamento con icona
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.IconLocation = "$IconPath,0"
$Shortcut.Save()

Write-Host ""
Write-Host "================================================"
Write-Host "ICONA APPLICATA CON SUCCESSO!"
Write-Host "================================================"
Write-Host ""
Write-Host "Collegamento: $ShortcutPath"
Write-Host "Icona: $IconPath"
Write-Host ""
Write-Host "L'icona mostra 'IT' con frecce per indicare traduzione."
Write-Host ""
Write-Host "================================================"

