# ⚡ Quick Start - Setup in 5 Minuti

## 🎯 Installazione Rapida

### Windows (PowerShell)

```powershell
# 1. Crea virtual environment
python -m venv venv

# 2. Attiva virtual environment
.\venv\Scripts\activate

# 3. Installa dipendenze
pip install -r requirements.txt

# 4. Scarica modelli di traduzione (richiede ~5 minuti)
python setup_models.py

# 5. Avvia applicazione
python src\main.py
```

### Linux/Mac (Terminal)

```bash
# 1. Crea virtual environment
python3 -m venv venv

# 2. Attiva virtual environment
source venv/bin/activate

# 3. Installa dipendenze
pip install -r requirements.txt

# 4. Scarica modelli di traduzione (richiede ~5 minuti)
python setup_models.py

# 5. Avvia applicazione
python src/main.py
```

## 🚀 Prossimi Avvii

### Metodo 1: Script Automatico

**Windows**: Doppio click su `run.bat`

**Linux/Mac**: 
```bash
./run.sh
```

### Metodo 2: Manuale

```bash
# Attiva venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Avvia
python src/main.py
```

## ✅ Verifica Installazione

```bash
python -c "import PyQt6, fitz, docx, argostranslate, reportlab; print('✅ OK')"
```

## 📝 Primo Utilizzo

1. **Gestisci Modelli**: Click su "📥 Gestisci Modelli" per vedere modelli installati
2. **Seleziona Lingua**: es. Inglese → Italiano
3. **Carica Documento**: Seleziona un PDF o DOCX di test
4. **Scegli Output**: Seleziona una cartella per il file tradotto
5. **Traduci**: Click su "🌍 Avvia Traduzione"

## 🆘 Problemi?

### Errore: "python non riconosciuto"
→ Installa Python da [python.org](https://python.org)

### Errore: "pip non riconosciuto"
→ Usa: `python -m pip install -r requirements.txt`

### Modelli non si installano
→ Verifica connessione internet durante `setup_models.py`

### GUI non si apre
→ Windows: Installa [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

## 📚 Documentazione Completa

- **Installazione Dettagliata**: Vedi `INSTALL.md`
- **Guida Utilizzo**: Vedi `USAGE.md`
- **Funzionalità**: Vedi `README.md`

---

**Pronto in 5 minuti! ⚡**

