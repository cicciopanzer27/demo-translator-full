# 🛠️ Guida Installazione Dettagliata

Questa guida fornisce istruzioni passo-passo per installare e configurare il Traduttore Documenti Legali Offline.

## 📋 Requisiti di Sistema

### Hardware Minimo
- **CPU**: Dual-core 2.0 GHz o superiore
- **RAM**: 4 GB (8 GB raccomandati)
- **Spazio Disco**: 2 GB liberi (per modelli + cache)

### Hardware Raccomandato
- **CPU**: Quad-core 2.5 GHz o superiore
- **RAM**: 8 GB o più
- **Spazio Disco**: 5 GB liberi
- **SSD**: Raccomandato per prestazioni migliori

### Software
- **Python**: 3.8, 3.9, 3.10, o 3.11
- **Sistema Operativo**: Windows 10/11, Linux, macOS 10.14+

## 🪟 Installazione su Windows

### 1. Installa Python

Se non hai Python installato:

1. Scarica Python da [python.org](https://www.python.org/downloads/)
2. **IMPORTANTE**: Durante l'installazione, seleziona "Add Python to PATH"
3. Verifica installazione aprendo PowerShell:

```powershell
python --version
```

### 2. Setup Progetto

```powershell
# Naviga nella cartella
cd C:\Users\[TUO_USERNAME]\Desktop\Apps_LAC\TRANSLATOR_LAC

# Crea virtual environment
python -m venv venv

# Attiva virtual environment
venv\Scripts\activate

# Aggiorna pip
python -m pip install --upgrade pip

# Installa dipendenze
pip install -r requirements.txt
```

### 3. Installa Modelli

```powershell
python setup_models.py
```

Attendi il completamento (può richiedere 5-10 minuti a seconda della connessione).

### 4. Avvia Applicazione

```powershell
python src/main.py
```

## 🐧 Installazione su Linux

### 1. Installa Dipendenze Sistema

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
sudo apt install python3-pyqt6
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-pip python3-virtualenv
sudo dnf install python3-qt6
```

### 2. Setup Progetto

```bash
cd ~/Desktop/Apps_LAC/TRANSLATOR_LAC

# Crea virtual environment
python3 -m venv venv

# Attiva virtual environment
source venv/bin/activate

# Aggiorna pip
pip install --upgrade pip

# Installa dipendenze
pip install -r requirements.txt
```

### 3. Installa Modelli

```bash
python setup_models.py
```

### 4. Avvia Applicazione

```bash
python src/main.py
```

## 🍎 Installazione su macOS

### 1. Installa Homebrew (se non presente)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Installa Python

```bash
brew install python@3.11
```

### 3. Setup Progetto

```bash
cd ~/Desktop/Apps_LAC/TRANSLATOR_LAC

# Crea virtual environment
python3 -m venv venv

# Attiva virtual environment
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt
```

### 4. Installa Modelli

```bash
python setup_models.py
```

### 5. Avvia Applicazione

```bash
python src/main.py
```

## 🔧 Installazione Manuale Modelli

Se `setup_models.py` non funziona, puoi installare manualmente:

```python
python

>>> import argostranslate.package
>>> argostranslate.package.update_package_index()
>>> available = argostranslate.package.get_available_packages()

# Vedi pacchetti disponibili
>>> for pkg in available:
...     print(f"{pkg.from_code} -> {pkg.to_code}: {pkg.from_name} -> {pkg.to_name}")

# Installa coppia specifica (esempio: en -> it)
>>> pkg_en_it = next(filter(lambda x: x.from_code == 'en' and x.to_code == 'it', available))
>>> pkg_en_it.install()

# Ripeti per altre coppie
>>> exit()
```

## 📦 Creazione Eseguibile (Opzionale)

Per creare un file .exe standalone:

### Windows

```powershell
# Installa PyInstaller
pip install pyinstaller

# Crea eseguibile
pyinstaller --onefile --windowed --name="TraduttoreLegale" --icon=resources/icons/app.ico src/main.py

# Eseguibile in: dist/TraduttoreLegale.exe
```

### Linux/macOS

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="TraduttoreLegale" src/main.py

# Eseguibile in: dist/TraduttoreLegale
```

## 🧪 Verifica Installazione

Per verificare che tutto sia installato correttamente:

```bash
python -c "
import PyQt6
import fitz
import docx
import argostranslate
import reportlab
print('✅ Tutte le dipendenze sono installate correttamente!')
"
```

## ❗ Risoluzione Problemi Comuni

### Problema: "pip non riconosciuto"

**Soluzione Windows:**
```powershell
python -m pip install -r requirements.txt
```

**Soluzione Linux/Mac:**
```bash
python3 -m pip install -r requirements.txt
```

### Problema: "ModuleNotFoundError: No module named 'PyQt6'"

**Soluzione:**
```bash
pip install PyQt6 --force-reinstall
```

### Problema: "Permission denied" su Linux

**Soluzione:**
```bash
chmod +x src/main.py
```

### Problema: Modelli non si scaricano

**Possibili cause:**
1. Firewall blocca download
2. Proxy aziendale
3. Problemi connessione

**Soluzione:**
- Disabilita temporaneamente firewall
- Configura proxy: `export http_proxy=http://proxy:port`
- Scarica modelli manualmente da [Argos Translate Packages](https://github.com/argosopentech/argospm-index)

### Problema: "Qt platform plugin could not be initialized"

**Soluzione Linux:**
```bash
sudo apt install libxcb-xinerama0 libxcb-cursor0
```

## 🔄 Aggiornamento

Per aggiornare il software:

```bash
# Attiva virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Aggiorna dipendenze
pip install -r requirements.txt --upgrade

# Riavvia applicazione
python src/main.py
```

## 🗑️ Disinstallazione

Per rimuovere completamente il software:

```bash
# Rimuovi virtual environment
rm -rf venv

# Rimuovi modelli Argos Translate
rm -rf ~/.local/share/argos-translate

# Rimuovi cache
rm -rf ~/.cache/argostranslate

# Opzionale: elimina cartella progetto
rm -rf TRANSLATOR_LAC
```

## 📞 Supporto

Se riscontri problemi durante l'installazione:

1. Verifica i requisiti di sistema
2. Leggi la sezione "Risoluzione Problemi"
3. Controlla i log in `logs/translator.log`
4. Apri un issue su GitHub con dettagli dell'errore

---

**Buona traduzione! 📄✨**

