# 📄 TRADUTTORE DOCUMENTI LEGALI OFFLINE

Sistema professionale per traduzione documenti legali (nativi e scannerizzati) completamente offline.

## ⚡ AVVIO RAPIDO

### **1. Crea Icona Desktop**
```bash
CREA_ICONA_DESKTOP.bat
```

### **2. Avvia l'Applicazione**
- Clicca sull'icona sul desktop
- OPPURE esegui: `python src\main.py`

### **3. Traduci un Documento**
1. Seleziona lingue (es: Inglese → Italiano)
2. Seleziona file PDF/DOCX
3. Seleziona cartella output
4. Clicca **TRADUCI**

---

## 🎯 DOCUMENTI TEST DISPONIBILI

Nella cartella **`documents demo`** trovi 4 PDF reali per testare:

| Documento | Tipo | Pagine | Tempo |
|-----------|------|--------|-------|
| Physitek Letter | Nativo | 3 | ~1 min |
| MCS TS PAI Sirio | Nativo | 18 | ~3 min |
| Distribution Contract Trotec | Scannerizzato | 21 | ~7 min |
| DOC040625 | Scannerizzato | 40 | ~12 min |

**Test Raccomandato:** Inizia con "Physitek Letter" per verificare rapidamente il funzionamento.

---

## 📚 DOCUMENTAZIONE

- **`docs/PRONTO_PER_TEST.md`** → Guida completa per i test
- **`docs/SISTEMA_COMPLETO_FUNZIONANTE.md`** → Documentazione tecnica
- **`docs/blueprint.md`** → Architettura sistema OCR

---

## 🔧 CARATTERISTICHE

✅ **Documenti Supportati:**
- PDF nativi (testo selezionabile)
- PDF scannerizzati (OCR automatico)
- DOCX

✅ **Tecnologie:**
- **OCR:** EasyOCR + Tesseract + OpenCV
- **Traduzione:** Argos Translate (offline)
- **GUI:** PyQt6 moderna

✅ **Capacità:**
- Rilevamento automatico tipo documento
- Pre-processing immagini avanzato
- Traduzione offline 100%
- Preservazione layout originale

---

## 🛠️ SETUP (Prima Installazione)

### **1. Installa Modelli Traduzione**
```bash
python scripts\install_models.py
```

### **2. Installa Componenti OCR (Opzionale)**
```bash
python scripts\install_ocr_dependencies.py
```

### **3. Test Sistema**
```bash
python tests\test_documenti_demo.py
```

---

## 📁 STRUTTURA PROGETTO

```
TRANSLATOR_LAC/
├── src/               # Codice sorgente
├── documents demo/    # Documenti test
├── tests/            # Script di test
├── scripts/          # Utilità installazione
├── docs/             # Documentazione
└── run.bat           # Avvio rapido
```

---

## 💡 SUGGERIMENTI

### **Per Documenti Scannerizzati:**
- Migliore qualità scansione = migliore OCR
- 300 DPI è l'ideale
- Evita scansioni inclinate o con ombre

### **Per Documenti Lunghi:**
- Sii paziente - il processo è accurato ma richiede tempo
- Non chiudere l'applicazione durante la traduzione

### **Per Migliori Risultati:**
- Usa documenti in inglese per migliori traduzioni
- Installa modelli linguistici aggiuntivi se necessario

---

## 🎉 PRONTO PER L'USO!

Il sistema è stato testato con i documenti demo ed è completamente funzionante.

**Inizia ora:** Avvia l'applicazione e testa con i documenti nella cartella `documents demo`!

---

## 📞 SUPPORTO

- **Log:** `logs/translator.log`
- **Test:** `python tests/test_documenti_demo.py`
- **Documentazione:** `docs/PRONTO_PER_TEST.md`
