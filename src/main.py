#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto di ingresso principale dell'applicazione
"""

import sys
import os
from pathlib import Path

# Setup encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Aggiungi il percorso src al path
sys.path.insert(0, str(Path(__file__).parent))

from ui.main_window import main

if __name__ == "__main__":
    main()