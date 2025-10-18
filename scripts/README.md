# 🚀 Scripts - Traduttore LAC

Scripts di utilità per il Traduttore Documenti Legali.

---

## 📋 File Disponibili

### **run_silent.vbs**
Script VBScript per avviare l'applicazione **senza mostrare il terminale**.

**Uso:**
```
Doppio click su run_silent.vbs
```

---

### **create_desktop_shortcut.ps1**
Crea collegamento sul Desktop di Windows.

**Uso:**
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\create_desktop_shortcut.ps1
```

---

### **create_icon.py**
Genera icona personalizzata (IT con frecce).

**Uso:**
```powershell
.\venv\Scripts\python.exe .\scripts\create_icon.py
```

**Requisiti:**
- Pillow (installato automaticamente)

---

### **update_shortcut_icon.ps1**
Applica icona personalizzata al collegamento desktop.

**Uso:**
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\update_shortcut_icon.ps1
```

---

## ⚡ Setup Rapido

### Metodo 1: Script Automatico (RACCOMANDATO)

Dalla directory principale del progetto:

```powershell
.\SETUP_DESKTOP.ps1
```

Questo esegue automaticamente:
1. ✅ Verifica ambiente
2. ✅ Crea icona
3. ✅ Crea collegamento
4. ✅ Applica icona

---

### Metodo 2: Manuale

```powershell
# Step 1: Crea icona
.\venv\Scripts\python.exe .\scripts\create_icon.py

# Step 2: Crea collegamento
powershell -ExecutionPolicy Bypass -File .\scripts\create_desktop_shortcut.ps1

# Step 3: Applica icona
powershell -ExecutionPolicy Bypass -File .\scripts\update_shortcut_icon.ps1
```

---

## 🎯 Risultato

Dopo l'esecuzione, troverai sul Desktop:

**📁 Traduttore LAC**
- Icona: Cerchio nero con "IT ↔" bianco
- Click: Apre GUI senza terminale
- Modalità: Silenzioso

---

## 🔧 Personalizzazione

### Cambiare Icona

Modifica `create_icon.py`:
```python
# Cambia colori
color='#000000'  # Sfondo nero
fill='#FFFFFF'   # Testo bianco

# Cambia testo
text_it = "IT"   # Modifica questo
```

### Cambiare Nome Collegamento

Modifica `create_desktop_shortcut.ps1`:
```powershell
$ShortcutPath = Join-Path $DesktopPath "Traduttore LAC.lnk"
#                                       ^^^^^^^^^^^^^^^^
#                                       Cambia questo nome
```

---

## ❓ Troubleshooting

### Errore: "Execution Policy"

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Collegamento non funziona

Verifica percorsi in `run_silent.vbs`:
```vbscript
projectPath = "C:\Users\jecho\Desktop\Apps_LAC\TRANSLATOR_LAC"
```

### Icona non visualizzata

1. Rinomina collegamento
2. Riavvia Explorer
3. Riapplica icona con `update_shortcut_icon.ps1`

---

## 📝 Note

- **VBScript** nasconde il terminale usando `WindowStyle = 0`
- **pythonw.exe** invece di python.exe (nessuna console)
- **Icona** in formato .ico multiplo (16x16 a 256x256)

---

## ✅ Vantaggi

✅ Avvio **silenzioso** (professionale)
✅ Icona **personalizzata** (riconoscibile)
✅ **Nessun terminale** visibile
✅ Esperienza utente **pulita**

---

