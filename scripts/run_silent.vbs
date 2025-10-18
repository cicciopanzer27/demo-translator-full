Set WshShell = CreateObject("WScript.Shell")

' Percorso alla directory del progetto
projectPath = "C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC"

' Percorso al Python virtual environment (con venv attivato)
pythonPath = projectPath & "\venv\Scripts\python.exe"

' Percorso allo script principale
scriptPath = projectPath & "\src\main.py"

' Cambia working directory al progetto (IMPORTANTE!)
WshShell.CurrentDirectory = projectPath

' Esegui Python senza mostrare finestra console
' 0 = nasconde la finestra, False = non aspetta
WshShell.Run """" & pythonPath & """ """ & scriptPath & """", 0, False

Set WshShell = Nothing

