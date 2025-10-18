#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interfaccia utente principale
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QComboBox, 
                             QTextEdit, QProgressBar, QFileDialog, QMessageBox,
                             QGroupBox, QGridLayout, QFrame)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon

# Aggiungi il percorso src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.document_processor import DocumentProcessor

class TranslationWorker(QThread):
    """Worker per traduzione in background"""
    
    progress = pyqtSignal(int, str)  # percent, message
    finished = pyqtSignal(dict)      # result
    error = pyqtSignal(str)          # error message
    
    def __init__(self, input_path, output_path, from_lang, to_lang):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.processor = DocumentProcessor()
    
    def run(self):
        """Esegue la traduzione"""
        try:
            result = self.processor.process_document(
                input_path=self.input_path,
                output_path=self.output_path,
                from_lang=self.from_lang,
                to_lang=self.to_lang,
                progress_callback=self.progress.emit
            )
            
            if result['success']:
                self.finished.emit(result)
            else:
                self.error.emit(result.get('error', 'Errore sconosciuto'))
                
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    """Finestra principale dell'applicazione"""
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()
    
    def init_ui(self):
        """Inizializza l'interfaccia utente"""
        
        self.setWindowTitle("Traduttore Documenti Legali Offline")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principale
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Titolo
        title_label = QLabel("TRADUTTORE DOCUMENTI LEGALI OFFLINE")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Sottotitolo
        subtitle_label = QLabel("Traduzione automatica di documenti PDF con preservazione layout")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        subtitle_label.setFont(subtitle_font)
        main_layout.addWidget(subtitle_label)
        
        # Separatore
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)
        
        # Gruppo selezione lingue
        lang_group = QGroupBox("Selezione Lingue")
        lang_layout = QHBoxLayout(lang_group)
        
        # Lingua sorgente
        lang_layout.addWidget(QLabel("Da:"))
        self.from_lang_combo = QComboBox()
        self.from_lang_combo.addItems(["en", "it"])
        self.from_lang_combo.setCurrentText("en")
        lang_layout.addWidget(self.from_lang_combo)
        
        # Freccia
        arrow_label = QLabel("→")
        arrow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lang_layout.addWidget(arrow_label)
        
        # Lingua destinazione
        lang_layout.addWidget(QLabel("A:"))
        self.to_lang_combo = QComboBox()
        self.to_lang_combo.addItems(["it", "en"])
        self.to_lang_combo.setCurrentText("it")
        lang_layout.addWidget(self.to_lang_combo)
        
        # Pulsante gestione modelli
        self.models_btn = QPushButton("Gestisci Modelli")
        self.models_btn.clicked.connect(self.manage_models)
        lang_layout.addWidget(self.models_btn)
        
        lang_layout.addStretch()
        main_layout.addWidget(lang_group)
        
        # Gruppo selezione file
        file_group = QGroupBox("Selezione Documento")
        file_layout = QVBoxLayout(file_group)
        
        # File input
        input_layout = QHBoxLayout()
        self.input_file_label = QLabel("Nessun file selezionato")
        self.input_file_label.setStyleSheet("color: #666; font-style: italic;")
        input_layout.addWidget(self.input_file_label)
        input_layout.addStretch()
        
        self.select_file_btn = QPushButton("Seleziona PDF")
        self.select_file_btn.clicked.connect(self.select_input_file)
        input_layout.addWidget(self.select_file_btn)
        file_layout.addLayout(input_layout)
        
        # Cartella output
        output_layout = QHBoxLayout()
        self.output_folder_label = QLabel("Cartella output: documents demo")
        self.output_folder_label.setStyleSheet("color: #666; font-style: italic;")
        output_layout.addWidget(self.output_folder_label)
        output_layout.addStretch()
        
        self.select_output_btn = QPushButton("Seleziona Cartella")
        self.select_output_btn.clicked.connect(self.select_output_folder)
        output_layout.addWidget(self.select_output_btn)
        file_layout.addLayout(output_layout)
        
        main_layout.addWidget(file_group)
        
        # Anteprima documento
        preview_group = QGroupBox("Anteprima Documento")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_text = QTextEdit()
        self.preview_text.setMaximumHeight(150)
        self.preview_text.setPlaceholderText("Il contenuto del documento apparirà qui...")
        preview_layout.addWidget(self.preview_text)
        
        main_layout.addWidget(preview_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Pulsante traduci
        self.translate_btn = QPushButton("TRADUCI")
        self.translate_btn.setMinimumHeight(50)
        self.translate_btn.setStyleSheet("""
            QPushButton {
                background-color: #2E8B57;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #228B22;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #666666;
            }
        """)
        self.translate_btn.clicked.connect(self.start_translation)
        main_layout.addWidget(self.translate_btn)
        
        # Inizializza variabili
        self.input_file = None
        self.output_folder = Path("documents demo")
        
    def select_input_file(self):
        """Seleziona file PDF di input"""
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona documento PDF",
            str(self.output_folder),
            "File PDF (*.pdf)"
        )
        
        if file_path:
            self.input_file = Path(file_path)
            self.input_file_label.setText(f"File: {self.input_file.name}")
            self.input_file_label.setStyleSheet("color: #000; font-style: normal;")
            
            # Mostra anteprima
            self.show_document_preview()
    
    def select_output_folder(self):
        """Seleziona cartella di output"""
        
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Seleziona cartella di output",
            str(self.output_folder)
        )
        
        if folder_path:
            self.output_folder = Path(folder_path)
            self.output_folder_label.setText(f"Cartella output: {self.output_folder.name}")
            self.output_folder_label.setStyleSheet("color: #000; font-style: normal;")
    
    def show_document_preview(self):
        """Mostra anteprima del documento"""
        
        if not self.input_file or not self.input_file.exists():
            return
        
        try:
            # Usa il processore per estrarre anteprima
            processor = DocumentProcessor()
            
            # Estrai solo la prima pagina per anteprima
            if processor._detect_document_type(str(self.input_file)) == "native":
                from extractors.pdf_native_extractor import PDFNativeExtractor
                extractor = PDFNativeExtractor()
                pages = extractor.extract_text_with_layout(str(self.input_file))
            else:
                from extractors.pdf_ocr_extractor import PDFOCRExtractor
                extractor = PDFOCRExtractor()
                pages = extractor.extract_text_with_ocr(str(self.input_file))
            
            if pages:
                preview_text = pages[0]['text'][:500] + "..." if len(pages[0]['text']) > 500 else pages[0]['text']
                self.preview_text.setPlainText(preview_text)
            else:
                self.preview_text.setPlainText("Impossibile estrarre anteprima del documento")
            
        except Exception as e:
            self.preview_text.setPlainText(f"Errore nell'anteprima: {str(e)}")
    
    def start_translation(self):
        """Avvia il processo di traduzione"""
        
        if not self.input_file or not self.input_file.exists():
            QMessageBox.warning(self, "Errore", "Seleziona un file PDF valido")
            return
        
        if not self.output_folder.exists():
            QMessageBox.warning(self, "Errore", "Seleziona una cartella di output valida")
            return
        
        # Prepara percorsi
        from_lang = self.from_lang_combo.currentText()
        to_lang = self.to_lang_combo.currentText()
        
        output_filename = f"{self.input_file.stem}_tradotto.docx"
        output_path = self.output_folder / output_filename
        
        # Disabilita controlli
        self.translate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Avvia worker
        self.worker = TranslationWorker(
            input_path=str(self.input_file),
            output_path=str(output_path),
            from_lang=from_lang,
            to_lang=to_lang
        )
        
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.translation_finished)
        self.worker.error.connect(self.translation_error)
        self.worker.start()
    
    def update_progress(self, percent, message):
        """Aggiorna la progress bar"""
        
        self.progress_bar.setValue(percent)
        self.statusBar().showMessage(message)
    
    def translation_finished(self, result):
        """Traduzione completata con successo"""
        
        self.progress_bar.setVisible(False)
        self.translate_btn.setEnabled(True)
        
        # Mostra messaggio di successo
        message = f"""Traduzione completata!

File generato: {Path(result['output_path']).name}
Pagine processate: {result['pages_processed']}
Caratteri tradotti: {result['total_chars']:,}
Parole tradotte: {result['total_words']:,}
Tipo documento: {result['doc_type']}"""

        QMessageBox.information(self, "Successo", message)
        
        # Aggiorna anteprima con testo tradotto
        try:
            from docx import Document
            doc = Document(result['output_path'])
            translated_text = ""
            for para in doc.paragraphs:
                translated_text += para.text + "\n"
            
            preview = translated_text[:500] + "..." if len(translated_text) > 500 else translated_text
            self.preview_text.setPlainText(f"TRADOTTO:\n\n{preview}")
        except:
            pass
    
    def translation_error(self, error_message):
        """Errore durante la traduzione"""
        
        self.progress_bar.setVisible(False)
        self.translate_btn.setEnabled(True)
        
        QMessageBox.critical(self, "Errore Traduzione", f"Si è verificato un errore:\n\n{error_message}")
    
    def manage_models(self):
        """Gestisce i modelli di traduzione"""
        
        QMessageBox.information(
            self,
            "Gestione Modelli", 
            "I modelli di traduzione vengono installati automaticamente al primo utilizzo.\n\n"
            "Modelli supportati:\n"
            "• Inglese ↔ Italiano\n"
            "• Installazione automatica offline"
        )

def main():
    """Funzione principale"""
    
    app = QApplication(sys.argv)
    app.setApplicationName("Traduttore Documenti Legali")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()