# 📋 Piano di Miglioramento Traduzione

## 🔍 **ANALISI PROBLEMI IDENTIFICATI**

### **Problemi Rilevati:**
1. **Grassetto problematico**: 19.4% del testo in grassetto causa errori di formattazione
2. **Font multipli**: 6 font diversi causano inconsistenze
3. **Testo maiuscolo**: Parole in maiuscolo (es. "EMAIL E MAIL REGISTRATO") 
4. **Documenti scansionati**: Alcuni PDF hanno 0 span di testo (immagini)
5. **Short bold**: Grassetto su testo corto causa problemi layout

### **Statistiche Attuali:**
- **Font più usati**: ArialMT (66.2%), Cambria (34.7%)
- **Grassetto originale**: 21.0% → **Tradotto**: 19.4% (miglioramento)
- **Problemi ridotti**: 19 → 10 (-47% problemi)

---

## 🛠️ **TOOL OPENSOURCE IDENTIFICATI**

### **1. OCR per Documenti Scansionati**
```python
# Tesseract OCR (Google)
pip install pytesseract pillow

# PaddleOCR (Baidu) - Migliore per multilangue
pip install paddlepaddle paddleocr

# EasyOCR - Più semplice da usare
pip install easyocr
```

### **2. Gestione Font e Formattazione**
```python
# FontTools per analisi font
pip install fonttools

# Pillow per manipolazione immagini
pip install pillow

# ReportLab per PDF avanzati
pip install reportlab
```

### **3. Parser Documenti Avanzati**
```python
# LayoutParser per layout detection
pip install layoutparser

# Unstructured per parsing intelligente
pip install unstructured[pdf]

# pdfplumber per estrazione testo strutturato
pip install pdfplumber
```

---

## 🎯 **MIGLIORAMENTI PROPOSTI**

### **FASE 1: OCR per Documenti Scansionati**

#### **A. Integrazione PaddleOCR**
```python
from paddleocr import PaddleOCR

def extract_text_scanned_pdf(pdf_path):
    """Estrai testo da PDF scansionato"""
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    
    # Converti PDF in immagini
    images = pdf_to_images(pdf_path)
    
    results = []
    for img in images:
        result = ocr.ocr(img, cls=True)
        results.extend(result)
    
    return results
```

#### **B. Rilevamento Automatico Tipo Documento**
```python
def detect_document_type(pdf_path):
    """Rileva se PDF è scansionato o con testo"""
    doc = fitz.open(pdf_path)
    
    text_content = ""
    for page in doc[:3]:  # Prime 3 pagine
        text_content += page.get_text()
    
    doc.close()
    
    # Se meno di 100 caratteri, probabilmente scansionato
    if len(text_content.strip()) < 100:
        return "scanned"
    else:
        return "text"
```

### **FASE 2: Miglioramento Gestione Font**

#### **A. Normalizzazione Font**
```python
def normalize_fonts(document):
    """Normalizza font per consistenza"""
    font_mapping = {
        'ArialMT': 'Arial',
        'Arial-BoldMT': 'Arial Bold',
        'Calibri-Bold': 'Calibri Bold',
        'Cambria': 'Cambria',
        'Cambria-Bold': 'Cambria Bold'
    }
    
    for para in document.paragraphs:
        for run in para.runs:
            if run.font.name in font_mapping:
                run.font.name = font_mapping[run.font.name]
```

#### **B. Gestione Grassetto Intelligente**
```python
def smart_bold_handling(text, original_bold_runs):
    """Gestisce grassetto in modo intelligente"""
    
    # Identifica parole chiave che dovrebbero essere in grassetto
    keywords = ['Art.', 'Article', 'Section', 'Clause', 'Contract']
    
    # Applica grassetto solo a parole chiave, non a tutto il testo
    for keyword in keywords:
        if keyword.lower() in text.lower():
            # Applica grassetto solo alla parola chiave
            return apply_selective_bold(text, keyword)
    
    return text
```

### **FASE 3: Parser Intelligente**

#### **A. Layout Detection**
```python
import layoutparser as lp

def detect_document_layout(pdf_path):
    """Rileva layout del documento"""
    model = lp.Detectron2LayoutModel('lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config')
    
    # Analizza layout
    layout = model.detect(pdf_path)
    
    # Classifica elementi
    elements = {
        'title': [],
        'paragraph': [],
        'list': [],
        'table': [],
        'figure': []
    }
    
    return elements
```

#### **B. Traduzione Contestuale**
```python
def translate_with_context(text, element_type, context):
    """Traduci considerando il contesto"""
    
    if element_type == 'title':
        # Traduzione più formale per titoli
        return translate_formal(text)
    elif element_type == 'list':
        # Mantieni struttura liste
        return translate_list_items(text)
    elif element_type == 'table':
        # Traduci solo contenuto, mantieni struttura
        return translate_table_content(text)
    else:
        # Traduzione standard
        return translate_standard(text)
```

---

## 🚀 **IMPLEMENTAZIONE PRIORITARIA**

### **1. OCR Integration (Priorità ALTA)**
- ✅ Aggiungi PaddleOCR per documenti scansionati
- ✅ Rilevamento automatico tipo documento
- ✅ Fallback intelligente (testo → OCR)

### **2. Font Normalization (Priorità MEDIA)**
- ✅ Mappatura font consistente
- ✅ Gestione grassetto selettiva
- ✅ Preservazione formattazione originale

### **3. Layout Parser (Priorità BASSA)**
- ✅ Rilevamento elementi documento
- ✅ Traduzione contestuale
- ✅ Preservazione struttura

---

## 📊 **METRICHE DI SUCCESSO**

### **Obiettivi:**
- **Documenti scansionati**: 0% → 100% processabili
- **Font consistency**: 6 font → 2-3 font principali
- **Bold issues**: 10 problemi → <5 problemi
- **Layout preservation**: 90% → 95%+

### **KPI:**
- Tempo traduzione: -20%
- Qualità traduzione: +15%
- Errori formattazione: -50%
- Documenti supportati: +100%

---

## 🔧 **PROSSIMI PASSI**

1. **Implementa OCR** per documenti scansionati
2. **Aggiungi font normalization** 
3. **Migliora gestione grassetto**
4. **Testa con documenti problematici**
5. **Ottimizza performance**

---

## 📚 **RISORSE AGGIUNTIVE**

- **PaddleOCR Docs**: https://github.com/PaddlePaddle/PaddleOCR
- **LayoutParser**: https://github.com/Layout-Parser/layout-parser
- **FontTools**: https://fonttools.readthedocs.io/
- **PDF Processing**: https://github.com/pdfplumber/pdfplumber

---

**Il piano si concentra sui problemi reali identificati nell'analisi e propone soluzioni concrete con tool opensource moderni.**
