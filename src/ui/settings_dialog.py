from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QProgressBar, QMessageBox,
    QGroupBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import logging
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from translation.engine import ModelManager

logger = logging.getLogger(__name__)

class ModelDownloadWorker(QThread):
    """Worker per download modelli in background"""
    
    progress = pyqtSignal(int, str)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, from_code, to_code):
        super().__init__()
        self.from_code = from_code
        self.to_code = to_code
    
    def run(self):
        try:
            ModelManager.install_language_pair(
                self.from_code,
                self.to_code,
                progress_callback=lambda v, t, m: self.progress.emit(v, m)
            )
            self.finished.emit()
        except Exception as e:
            logger.exception("Errore download modello")
            self.error.emit(str(e))


class ModelsDialog(QDialog):
    """Dialog per gestione modelli traduzione"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Gestione Modelli di Traduzione')
        self.setGeometry(200, 200, 600, 500)
        self.worker = None
        
        self.init_ui()
        self.load_available_packages()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel('Scarica Modelli di Traduzione Offline')
        header.setStyleSheet('font-size: 16px; font-weight: bold; padding: 10px;')
        layout.addWidget(header)
        
        info = QLabel(
            'Seleziona le coppie di lingue da installare.\n'
            'I modelli verranno scaricati e installati localmente.'
        )
        info.setWordWrap(True)
        info.setStyleSheet('color: gray; padding: 5px;')
        layout.addWidget(info)
        
        # Lista modelli disponibili
        group = QGroupBox("Modelli Disponibili")
        group_layout = QVBoxLayout(group)
        
        self.models_list = QListWidget()
        group_layout.addWidget(self.models_list)
        
        layout.addWidget(group)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton('🔄 Aggiorna Lista')
        self.refresh_btn.clicked.connect(self.load_available_packages)
        btn_layout.addWidget(self.refresh_btn)
        
        self.download_btn = QPushButton('📥 Scarica Selezionato')
        self.download_btn.clicked.connect(self.download_selected)
        btn_layout.addWidget(self.download_btn)
        
        self.close_btn = QPushButton('Chiudi')
        self.close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.close_btn)
        
        layout.addLayout(btn_layout)
    
    def load_available_packages(self):
        """Carica lista pacchetti disponibili"""
        self.status_label.setText('Caricamento pacchetti disponibili...')
        self.models_list.clear()
        
        try:
            # Aggiorna indice
            ModelManager.update_package_index()
            
            # Ottieni pacchetti
            packages = ModelManager.get_available_packages()
            
            # Popola lista
            for pkg in packages:
                item_text = f"{pkg.from_name} → {pkg.to_name} ({pkg.from_code} → {pkg.to_code})"
                self.models_list.addItem(item_text)
                # Store metadata
                item = self.models_list.item(self.models_list.count() - 1)
                item.setData(Qt.ItemDataRole.UserRole, (pkg.from_code, pkg.to_code))
            
            self.status_label.setText(f'{len(packages)} modelli disponibili')
            
        except Exception as e:
            logger.exception("Errore caricamento pacchetti")
            self.status_label.setText(f'Errore: {e}')
            QMessageBox.warning(self, 'Errore', f'Errore caricamento pacchetti:\n{e}')
    
    def download_selected(self):
        """Scarica modello selezionato"""
        current_item = self.models_list.currentItem()
        
        if not current_item:
            QMessageBox.warning(self, 'Attenzione', 'Seleziona un modello da scaricare')
            return
        
        # Ottieni codici lingua
        from_code, to_code = current_item.data(Qt.ItemDataRole.UserRole)
        
        # Conferma
        reply = QMessageBox.question(
            self,
            'Conferma Download',
            f'Scaricare modello {from_code} → {to_code}?\n\n'
            'Il download potrebbe richiedere alcuni minuti.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Disabilita UI
        self.download_btn.setEnabled(False)
        self.refresh_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Avvia download
        self.worker = ModelDownloadWorker(from_code, to_code)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.download_finished)
        self.worker.error.connect(self.download_error)
        self.worker.start()
    
    def update_progress(self, value: int, message: str):
        """Aggiorna progress bar"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
    
    def download_finished(self):
        """Download completato"""
        self.progress_bar.setVisible(False)
        self.status_label.setText('✅ Modello installato con successo!')
        
        QMessageBox.information(
            self,
            'Completato',
            'Modello installato correttamente.\n\nOra puoi usarlo per tradurre documenti.'
        )
        
        # Riabilita UI
        self.download_btn.setEnabled(True)
        self.refresh_btn.setEnabled(True)
    
    def download_error(self, error_msg: str):
        """Errore download"""
        self.progress_bar.setVisible(False)
        self.status_label.setText('❌ Errore download')
        
        QMessageBox.critical(
            self,
            'Errore',
            f'Errore durante il download:\n\n{error_msg}'
        )
        
        # Riabilita UI
        self.download_btn.setEnabled(True)
        self.refresh_btn.setEnabled(True)

