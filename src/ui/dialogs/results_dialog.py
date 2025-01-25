from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtCore import Qt, QSize
from ui.styles.style import COLORS, FONTS
import csv

DIALOG_STYLES = {
    "dialog": f"""
        QDialog {{
            background-color: {COLORS['secondary']};
            border: 5px solid {COLORS['border']};
            border-radius: 15px;
            margin: 0px;
        }}
    """,
    "table": f"""
        QTableWidget {{
            background-color: white;
            border: 2px solid {COLORS['border']};
            border-radius: 5px;
            gridline-color: {COLORS['border']};
            font-family: "Courier New";
            font-size: 14px;
        }}
        QTableWidget::item {{
            padding: 5px;
        }}
        QHeaderView::section {{
            background-color: {COLORS['primary']};
            color: white;
            font-family: "Courier New";
            font-size: 14px;
            font-weight: bold;
            padding: 5px;
            border: none;
        }}
        QScrollBar:vertical {{
            border: none;
            background: {COLORS['border']};
            width: 10px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {COLORS['border']};
            min-height: 20px;
            border-radius: 5px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
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
            min-width: 120px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['primary']};
        }}
    """,
    "max_button": f"""
        QPushButton {{
            background-color: transparent;
            border: none;
            color: {COLORS['border']};
            font-size: 16px;
            font-weight: bold;
            padding: 5px;
            min-width: 30px;
            max-width: 30px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['accent']};
            color: white;
            border-radius: 5px;
        }}
    """,
}


class ResultsDialog(QDialog):
    def __init__(self, parent=None, results=None):
        super().__init__(parent)
        self.setWindowTitle("Resultados de la Búsqueda")
        self.setMinimumSize(800, 600)
        # Habilitar botones de maximizar/minimizar en la barra de título
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowCloseButtonHint
            | Qt.WindowType.WindowMaximizeButtonHint
            | Qt.WindowType.WindowMinimizeButtonHint
        )
        self.setStyleSheet(DIALOG_STYLES["dialog"])
        self.results = results or []
        self.is_maximized = False

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Título
        title = QLabel("Resultados Encontrados")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(FONTS["normal"])
        layout.addWidget(title)

        # Tabla
        self.table = QTableWidget()
        self.table.setStyleSheet(DIALOG_STYLES["table"])
        layout.addWidget(self.table)

        # Botones inferiores
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setSpacing(20)

        export_button = QPushButton("Exportar a CSV")
        export_button.setStyleSheet(DIALOG_STYLES["button"])
        export_button.clicked.connect(self.export_to_csv)
        export_button.setCursor(Qt.CursorShape.PointingHandCursor)

        close_button = QPushButton("Cerrar")
        close_button.setStyleSheet(DIALOG_STYLES["button"])
        close_button.clicked.connect(self.accept)
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)

        button_layout.addWidget(export_button)
        button_layout.addWidget(close_button)
        layout.addWidget(button_container)

        # Llenar la tabla
        self.populate_table()

    def populate_table(self):
        if not self.results:
            return

        # Configurar columnas
        headers = ["Archivo"] + list(self.results[0].keys())
        headers.remove("archivo")  # Quitamos "archivo" porque ya lo añadimos primero
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # Añadir filas
        self.table.setRowCount(len(self.results))
        for row, result in enumerate(self.results):
            # Añadir nombre del archivo
            file_item = QTableWidgetItem(result["archivo"])
            self.table.setItem(row, 0, file_item)

            # Añadir los demás datos
            for col, key in enumerate(headers[1:], 1):
                item = QTableWidgetItem(str(result.get(key, "No encontrado")))
                self.table.setItem(row, col, item)

        # Ajustar tamaño de columnas
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def export_to_csv(self):
        """Exporta los resultados a un archivo CSV"""
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        file_dialog.setDefaultSuffix("csv")
        file_dialog.setWindowTitle("Guardar Resultados")

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            try:
                with open(file_path, "w", newline="", encoding="utf-8") as f:
                    # Obtener encabezados
                    headers = ["Archivo"] + [
                        col for col in self.results[0].keys() if col != "archivo"
                    ]
                    writer = csv.writer(f)
                    writer.writerow(headers)

                    # Escribir datos
                    for result in self.results:
                        row = [result["archivo"]]
                        row.extend(
                            result.get(key, "No encontrado") for key in headers[1:]
                        )
                        writer.writerow(row)

                QMessageBox.information(
                    self, "Éxito", f"Archivo guardado exitosamente en:\n{file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Error al guardar el archivo: {str(e)}"
                )
