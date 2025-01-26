from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QWidget,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import os
from ui.styles.style import COLORS
import pandas as pd

DIALOG_STYLES = {
    "dialog": f"""
        QDialog {{
            background-color: {COLORS['secondary']};
            border: 5px solid {COLORS['border']};
            border-radius: 15px;
            margin: 0px;
        }}
    """,
    "message": f"""
        QLabel {{
            color: {COLORS['text']};
            font-family: "Courier New";
            font-size: 14px;
            padding: 10px;
        }}
    """,
    "file_label": f"""
        QLabel {{
            color: {COLORS['text']};
            font-family: "Courier New";
            font-size: 12px;
            padding: 5px;
            background-color: white;
            border: 1px solid {COLORS['border']};
            border-radius: 5px;
        }}
    """,
    "button": f"""
        QPushButton {{
            background-color: {COLORS['accent']};
            color: {COLORS['button_text']};
            font-family: "Courier New";
            border-radius: 15px;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLORS['primary']};
        }}
    """,
    "browse_button": f"""
        QPushButton {{
            background-color: {COLORS['primary']};
            color: {COLORS['button_text']};
            font-family: "Courier New";
            border-radius: 5px;
            padding: 5px 10px;
            font-size: 20px;
            font-weight: bold;
            min-width: 40px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['accent']};
        }}
    """,
}


class ExcelImportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Importar Campos desde Excel")
        self.setFixedSize(500, 250)
        self.setStyleSheet(DIALOG_STYLES["dialog"])
        self.search_terms = []

        # Establecer el ícono
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "resources",
            "images",
            "logo.ico",
        )
        self.setWindowIcon(QIcon(icon_path))

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Mensaje con salto de línea para mejor legibilidad
        message = QLabel("Seleccione un archivo Excel\ncon los campos a buscar")
        message.setStyleSheet(DIALOG_STYLES["message"])
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(message)

        # Contenedor para selección de archivo
        file_container = QWidget()
        file_layout = QHBoxLayout(file_container)
        file_layout.setSpacing(10)

        # Etiqueta para mostrar archivo seleccionado
        self.file_label = QLabel("Ningún archivo seleccionado")
        self.file_label.setStyleSheet(DIALOG_STYLES["file_label"])
        file_layout.addWidget(self.file_label)

        # Botón examinar (ajustado el tamaño)
        browse_button = QPushButton("...")
        browse_button.setStyleSheet(DIALOG_STYLES["browse_button"])
        browse_button.setFixedSize(30, 30)
        browse_button.clicked.connect(self.browse_file)
        browse_button.setCursor(Qt.CursorShape.PointingHandCursor)
        file_layout.addWidget(browse_button)

        layout.addWidget(file_container)

        # Botón importar (ajustado el tamaño)
        self.import_button = QPushButton("Importar")
        self.import_button.setStyleSheet(DIALOG_STYLES["button"])
        self.import_button.setFixedWidth(100)
        self.import_button.clicked.connect(self.import_terms)
        self.import_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.import_button.setEnabled(False)

        # Centrar el botón de importar
        import_container = QWidget()
        import_layout = QHBoxLayout(import_container)
        import_layout.addStretch()
        import_layout.addWidget(self.import_button)
        import_layout.addStretch()

        layout.addWidget(import_container)
        layout.addStretch()

    def browse_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Excel Files (*.xlsx *.xls)")
        file_dialog.setWindowTitle("Seleccionar Archivo Excel")

        if file_dialog.exec():
            self.excel_file = file_dialog.selectedFiles()[0]
            self.file_label.setText(self.excel_file.split("/")[-1])
            self.import_button.setEnabled(True)

    def import_terms(self):
        try:
            # Leer la primera columna del Excel
            df = pd.read_excel(self.excel_file, usecols=[0])
            # Obtener los términos no vacíos
            self.search_terms = [
                str(term).strip()
                for term in df.iloc[:, 0].dropna().tolist()
                if str(term).strip()
            ]

            if self.search_terms:
                self.accept()
            else:
                raise ValueError("No se encontraron términos válidos en el Excel")

        except Exception as e:
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.critical(
                self, "Error", f"Error al importar el archivo Excel: {str(e)}"
            )
