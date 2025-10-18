# 📖 Guida Utente - Traduttore Documenti Legali

## 🚀 Avvio Rapido

### 1. Prima Installazione
```bash
# Esegui il file di installazione
INSTALLA_DIPENDENZE.bat
```

### 2. Avvio Applicazione
```bash
# Doppio click su:
AVVIA_APPLICAZIONE.bat
```

## 🎯 Come Usare l'Applicazione

### Passo 1: Selezione Lingue
- **Da:** Scegli la lingua del documento originale
- **A:** Scegli la lingua di destinazione
- **Gestisci Modelli:** Installa modelli di traduzione

### Passo 2: Selezione Documento
- **Seleziona PDF:** Scegli il documento da tradurre
- **Seleziona Cartella:** Scegli dove salvare il risultato

### Passo 3: Traduzione
- **Anteprima:** Controlla il contenuto estratto
- **TRADUCI:** Avvia il processo di traduzione
- **Progress:** Segui l'avanzamento in tempo reale

## 📋 Tipi di Documenti Supportati

### ✅ Documenti PDF Nativi
- **Caratteristiche:** Testo selezionabile
- **Tempo:** 30 secondi - 4 minuti
- **Qualità:** Eccellente

### ✅ Documenti PDF Scannerizzati
- **Caratteristiche:** Immagini di testo
- **Tempo:** 2-8 minuti
- **Qualità:** Buona (dipende dalla qualità scan)

## 🔧 Risoluzione Problemi

### Problema: "Modelli non disponibili"
**Soluzione:**
1. Clicca "Gestisci Modelli"
2. Attendi installazione automatica
3. Riavvia l'applicazione

### Problema: "Errore OCR"
**Soluzione:**
1. Verifica che il PDF non sia corrotto
2. Prova con un documento più semplice
3. Controlla la qualità della scansione

### Problema: "Traduzione lenta"
**Soluzione:**
1. Chiudi altre applicazioni
2. Usa documenti più piccoli
3. Verifica spazio disco disponibile

## 📊 Prestazioni Attese

| Tipo Documento | Pagine | Tempo Stimato |
|----------------|--------|---------------|
| PDF Nativo | 1-5 | 30-90 sec |
| PDF Nativo | 6-20 | 1-4 min |
| PDF Scannerizzato | 1-5 | 2-4 min |
| PDF Scannerizzato | 6-20 | 4-8 min |

## 💡 Suggerimenti per Migliori Risultati

### Per Documenti Nativi:
- ✅ Usa PDF di buona qualità
- ✅ Evita documenti con troppi elementi grafici
- ✅ Verifica che il testo sia selezionabile

### Per Documenti Scannerizzati:
- ✅ Scansiona ad alta risoluzione (300 DPI+)
- ✅ Usa contrasto elevato
- ✅ Evita pagine storte o sfocate

## 📁 Struttura File Output

```
output/
├── nome_documento_tradotto.docx
└── output_YYYYMMDD/
    ├── documento1_tradotto.docx
    └── documento2_tradotto.docx
```

## 🆘 Supporto Tecnico

### Log di Sistema
- **Posizione:** `logs/translator.log`
- **Contenuto:** Dettagli errori e operazioni

### Test Sistema
```bash
# Esegui test completo
python _TESTS\test_nuovo_sistema.py
```

### Pulizia Progetto
```bash
# Pulisci file temporanei
python _SCRIPTS\pulisci_progetto.py
```

## 📞 Contatti

Per problemi tecnici o domande:
1. Consulta questa guida
2. Controlla i log di sistema
3. Esegui i test diagnostici
