# Script per creare collegamento desktop per Traduttore LAC

$WshShell = New-Object -ComObject WScript.Shell

# Percorsi
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Traduttore LAC.lnk"
$ProjectPath = "C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC"
$VBSPath = Join-Path $ProjectPath "scripts\run_silent.vbs"

# Crea collegamento
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $VBSPath
$Shortcut.WorkingDirectory = Join-Path $ProjectPath "scripts"
$Shortcut.WindowStyle = 1
$Shortcut.Description = "Traduttore Documenti Legali Offline - Italiano Centrale"

# Icona (opzionale - usa icona Python o personalizzata)
# $Shortcut.IconLocation = "C:\Path\To\Icon.ico,0"

$Shortcut.Save()

Write-Host ""
Write-Host "================================================"
Write-Host "COLLEGAMENTO CREATO CON SUCCESSO!"
Write-Host "================================================"
Write-Host ""
Write-Host "Posizione: $ShortcutPath"
Write-Host "Nome: Traduttore LAC"
Write-Host ""
Write-Host "Il collegamento apre l'applicazione SENZA mostrare il terminale."
Write-Host ""
Write-Host "================================================"

