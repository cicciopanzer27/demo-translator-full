"""Modern White & Black UI Styles"""

# Main Window Background
MAIN_WINDOW_STYLE = """
    QMainWindow {
        background-color: #000000;
    }
"""

# White Frame Style (per sezioni)
WHITE_FRAME_STYLE = """
    QFrame {
        background-color: #FFFFFF;
        border-radius: 8px;
    }
"""

# Radio Button Style (Black & White)
RADIO_BUTTON_STYLE = """
    QRadioButton {
        color: #000000;
        font-size: 14px;
        font-weight: bold;
        spacing: 10px;
    }
    QRadioButton::indicator {
        width: 20px;
        height: 20px;
    }
    QRadioButton::indicator:unchecked {
        border: 2px solid #000000;
        border-radius: 10px;
        background: #FFFFFF;
    }
    QRadioButton::indicator:checked {
        border: 2px solid #000000;
        border-radius: 10px;
        background: #000000;
    }
"""

# Primary Button Style (White on Black background)
PRIMARY_BUTTON_STYLE = """
    QPushButton {
        background-color: #FFFFFF;
        color: #000000;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #DDDDDD;
    }
    QPushButton:pressed {
        background-color: #CCCCCC;
    }
    QPushButton:disabled {
        background-color: #333333;
        color: #666666;
    }
"""

# Secondary Button Style (Black buttons in white frames)
SECONDARY_BUTTON_STYLE = """
    QPushButton {
        background-color: #000000;
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
    }
    QPushButton:hover {
        background-color: #333333;
    }
    QPushButton:pressed {
        background-color: #555555;
    }
"""

# Gestisci Modelli Button (Blue accent)
ACCENT_BUTTON_STYLE = """
    QPushButton {
        background-color: #3b82f6;
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #2563eb;
    }
    QPushButton:pressed {
        background-color: #1d4ed8;
    }
    QPushButton:disabled {
        background-color: #94a3b8;
        color: #cbd5e1;
    }
"""

# Progress Bar Style (White on dark background)
PROGRESS_BAR_STYLE = """
    QProgressBar {
        border: none;
        background-color: #333333;
        border-radius: 4px;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #FFFFFF;
        border-radius: 4px;
    }
"""

# ComboBox Style (for language selectors)
COMBOBOX_STYLE = """
    QComboBox {
        background-color: #FFFFFF;
        color: #000000;
        border: 2px solid #000000;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 13px;
        font-weight: bold;
    }
    QComboBox:hover {
        border-color: #333333;
    }
    QComboBox::drop-down {
        border: none;
        width: 30px;
    }
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid #000000;
        margin-right: 10px;
    }
    QComboBox QAbstractItemView {
        background-color: #FFFFFF;
        color: #000000;
        selection-background-color: #000000;
        selection-color: #FFFFFF;
        border: 2px solid #000000;
    }
"""

# GroupBox Style
GROUPBOX_STYLE = """
    QGroupBox {
        font-weight: bold;
        border: 2px solid #FFFFFF;
        border-radius: 8px;
        margin-top: 10px;
        padding-top: 15px;
        color: #FFFFFF;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 5px 10px;
        color: #FFFFFF;
    }
"""

# Text Edit / Preview Style
TEXT_EDIT_STYLE = """
    QTextEdit {
        background-color: #1a1a1a;
        color: #FFFFFF;
        border: 1px solid #333333;
        border-radius: 6px;
        padding: 10px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 11px;
    }
    QTextEdit:focus {
        border-color: #FFFFFF;
    }
"""

# Label Styles
TITLE_LABEL_STYLE = "color: #FFFFFF; font-size: 24px; font-weight: bold;"
SUBTITLE_LABEL_STYLE = "color: #888888; font-size: 13px;"
STATUS_LABEL_STYLE = "color: #888888; font-size: 11px;"
SUCCESS_LABEL_STYLE = "color: #00FF00; font-weight: bold;"
ERROR_LABEL_STYLE = "color: #FF0000; font-weight: bold;"

# File label styles (in white frames)
FILE_LABEL_INACTIVE = "color: #666666; font-size: 10px;"
FILE_LABEL_ACTIVE = "color: #000000; font-weight: bold; font-size: 10px;"


