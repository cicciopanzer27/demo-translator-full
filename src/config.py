#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurazione dell'applicazione
"""

import os
from pathlib import Path

# Percorsi principali
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = BASE_DIR / "src"
DOCS_DIR = BASE_DIR / "documents demo"
OUTPUT_DIR = BASE_DIR / "output"
MODELS_DIR = BASE_DIR / "models"

# Crea cartelle se non esistono
OUTPUT_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# Configurazione traduzione
SUPPORTED_LANGUAGES = {
    'it': 'Italiano',
    'en': 'Inglese'
}

# Configurazione OCR
OCR_LANGUAGES = ['en', 'it']
OCR_CONFIDENCE_THRESHOLD = 0.5

# Configurazione documenti
MAX_CHUNK_SIZE = 1000
MAX_PREVIEW_LENGTH = 500

# Configurazione UI
WINDOW_TITLE = "Traduttore Documenti Legali Offline"
WINDOW_SIZE = (800, 600)

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
