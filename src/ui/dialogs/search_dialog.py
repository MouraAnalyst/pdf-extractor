from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QWidget,
    QScrollArea,
    QFrame,
)
from PySide6.QtCore import Qt
from pdf_processor.pdf_extractor import PDFExtractor
from ui.styles.style import COLORS, FONTS
from .excel_import_dialog import ExcelImportDialog

# Estilos específicos para el diálogo
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
            font-size: 16px;
            font-weight: bold;
            padding: 15px;
            margin: 10px;
        }}
    """,
    "field": f"""
        QLineEdit {{
            font-family: "Courier New";
            font-size: 14px;
            padding: 10px;
            border: 2px solid {COLORS['border']};
            border-radius: 10px;
            margin: 5px;
        }}
    """,
    "add_button": f"""
        QPushButton {{
            background-color: {COLORS['primary']};
            color: {COLORS['button_text']};
            font-family: "Courier New";
            border-radius: 15px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLORS['accent']};
        }}
    """,
    "plus_button": f"""
        QPushButton {{
            background-color: #4CAF50;
            color: {COLORS['border']};
            border-radius: 15px;
            font-size: 20px;
            font-weight: bold;
            min-width: 30px;
            max-width: 30px;
            min-height: 30px;
            max-height: 30px;
        }}
        QPushButton:hover {{
            background-color: #45a049;
        }}
    """,
    "search_button": f"""
        QPushButton {{
            background-color: {COLORS['accent']};
            color: {COLORS['button_text']};
            font-family: "Courier New";
            border-radius: 15px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            margin: 10px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['primary']};
        }}
    """,
    "confirm_button": f"""
        QPushButton {{
            background-color: {COLORS['accent']};
            color: white;
            border-radius: 15px;
            font-size: 14px;
            font-weight: bold;
            min-width: 30px;
            max-width: 30px;
            min-height: 30px;
            max-height: 30px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['primary']};
        }}
    """,
    "confirmed_item": f"""
        QLabel {{
            color: #4a4a4a;
            font-family: "Courier New";
            font-size: 16px;
            padding: 5px 10px;
            background-color: transparent;
            font-weight: bold;
            margin: 5px;
        }}
    """,
    "edit_button": f"""
        QPushButton {{
            background-color: {COLORS['accent']};
            color: white;
            border-radius: 5px;
            padding: 2px 6px;
            font-size: 11px;
            font-weight: bold;
            min-width: 40px;
            max-width: 45px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['primary']};
        }}
    """,
    "arrow_label": f"""
        QLabel {{
            color: {COLORS['border']};
            font-family: "Courier New";
            font-size: 16px;
            background-color: transparent;
            font-weight: bold;
            margin: 0px 5px;
        }}
    """,
    "separator_line": f"""
        QFrame {{
            background-color: #E0E0E0;
            border: none;
            height: 1px;
            opacity: 0.5;
        }}
    """,
    "exclude_button": f"""
        QPushButton {{
            background-color: #ff4444;
            color: white;
            border-radius: 5px;
            padding: 2px 6px;
            font-size: 11px;
            font-weight: bold;
            min-width: 50px;
            max-width: 55px;
        }}
        QPushButton:hover {{
            background-color: #cc0000;
        }}
    """,
}


class SearchDialog(QDialog):
    def __init__(self, parent=None, pdf_files=None):
        super().__init__(parent)
        self.pdf_files = pdf_files or []
        self.search_fields = {}
        self.search_results = None

        self.setWindowTitle("Búsqueda en PDFs")
        self.setFixedSize(500, 400)  # Tamaño fijo
        self.setStyleSheet(DIALOG_STYLES["dialog"])

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Área scrollable
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(
            f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
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
        """
        )

        # Widget contenedor para los campos
        content_widget = QWidget()
        self.layout = QVBoxLayout(content_widget)
        self.layout.setSpacing(15)

        # Contenedor para botones de añadir
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setSpacing(10)

        # Botón Añadir Campo
        self.add_button = QPushButton("Añadir Campo")
        self.add_button.setStyleSheet(DIALOG_STYLES["add_button"])
        self.add_button.clicked.connect(self.add_search_field)
        self.add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        buttons_layout.addWidget(self.add_button)

        # Botón Masivo
        massive_button = QPushButton("Masivo")
        massive_button.setStyleSheet(DIALOG_STYLES["add_button"])
        massive_button.clicked.connect(self.import_from_excel)
        massive_button.setCursor(Qt.CursorShape.PointingHandCursor)
        buttons_layout.addWidget(massive_button)

        self.layout.addWidget(buttons_container)

        # Contenedor para campos de búsqueda
        self.fields_container = QWidget()
        self.fields_layout = QVBoxLayout(self.fields_container)
        self.fields_layout.setSpacing(1)
        self.layout.addWidget(self.fields_container)

        # Configurar el área scrollable
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # Botón de búsqueda
        self.search_button = QPushButton("Buscar")
        self.search_button.setStyleSheet(DIALOG_STYLES["search_button"])
        self.search_button.clicked.connect(self.perform_search)
        self.search_button.hide()
        main_layout.addWidget(self.search_button)

    def add_search_field(self):
        # Crear contenedor para el campo
        field_container = QWidget()
        field_layout = QHBoxLayout(field_container)
        field_layout.setContentsMargins(0, 0, 0, 0)

        # Campo de texto
        text_field = QLineEdit()
        text_field.setStyleSheet(DIALOG_STYLES["field"])
        text_field.setPlaceholderText("Ingrese el término a buscar")
        # Conectar la señal returnPressed (tecla Enter) con la confirmación
        text_field.returnPressed.connect(
            lambda: self.confirm_field(field_container, text_field)
        )
        field_layout.addWidget(text_field)

        # Botón de confirmar
        confirm_button = QPushButton("✔")
        confirm_button.setStyleSheet(DIALOG_STYLES["confirm_button"])
        confirm_button.clicked.connect(
            lambda: self.confirm_field(field_container, text_field)
        )
        field_layout.addWidget(confirm_button)

        # Añadir al contenedor principal al inicio
        self.fields_layout.insertWidget(0, field_container)

        # Ocultar el botón de añadir campo
        self.add_button.hide()

    def confirm_field(self, container, text_field):
        search_term = text_field.text().strip()
        if not search_term:
            return

        # Crear contenedor para el campo confirmado
        confirmed_container = QWidget()
        confirmed_layout = QHBoxLayout(confirmed_container)
        confirmed_layout.setContentsMargins(0, 0, 0, 0)
        confirmed_layout.setSpacing(5)

        # Flecha primero
        arrow = QLabel("➡️")
        arrow.setStyleSheet(DIALOG_STYLES["arrow_label"])
        confirmed_layout.addWidget(arrow)

        # Texto del campo
        label = QLabel(search_term)
        label.setStyleSheet(DIALOG_STYLES["confirmed_item"])
        confirmed_layout.addWidget(label)

        # Espacio flexible para empujar los botones a la derecha
        confirmed_layout.addStretch()

        # Botón editar
        edit_button = QPushButton("Editar")
        edit_button.setStyleSheet(DIALOG_STYLES["edit_button"])
        edit_button.clicked.connect(
            lambda: self.edit_field(confirmed_container, search_term)
        )
        edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        confirmed_layout.addWidget(edit_button)

        # Botón excluir
        exclude_button = QPushButton("Excluir")
        exclude_button.setStyleSheet(DIALOG_STYLES["exclude_button"])
        exclude_button.clicked.connect(
            lambda: self.exclude_field(confirmed_container, search_term)
        )
        exclude_button.setCursor(Qt.CursorShape.PointingHandCursor)
        confirmed_layout.addWidget(exclude_button)

        # Línea separadora
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(DIALOG_STYLES["separator_line"])

        # Guardar el término de búsqueda
        self.search_fields[search_term] = search_term

        # Obtener el índice del contenedor actual
        index = self.fields_layout.indexOf(container)

        # Añadir el campo confirmado y luego el separador
        self.fields_layout.insertWidget(index + 1, confirmed_container)
        self.fields_layout.insertWidget(index + 2, separator)
        container.deleteLater()

        # Mostrar botón de añadir campo y buscar
        self.add_button.show()
        self.search_button.show()

    def edit_field(self, container, old_term):
        # Eliminar el término del diccionario
        self.search_fields.pop(old_term, None)

        # Crear nuevo campo de edición
        field_container = QWidget()
        field_layout = QHBoxLayout(field_container)
        field_layout.setContentsMargins(0, 0, 0, 0)

        text_field = QLineEdit()
        text_field.setStyleSheet(DIALOG_STYLES["field"])
        text_field.setText(old_term)
        field_layout.addWidget(text_field)

        confirm_button = QPushButton("✔")
        confirm_button.setStyleSheet(DIALOG_STYLES["confirm_button"])
        confirm_button.clicked.connect(
            lambda: self.confirm_field(field_container, text_field)
        )
        field_layout.addWidget(confirm_button)

        # Reemplazar el campo confirmado
        index = self.fields_layout.indexOf(container)
        if index > 0:  # Si hay un separador antes del campo
            separator = self.fields_layout.itemAt(index - 1).widget()
            separator.deleteLater()
        self.fields_layout.replaceWidget(container, field_container)
        container.deleteLater()

        # Ocultar botón de añadir campo
        self.add_button.hide()

    def perform_search(self):
        if not self.search_fields:
            return

        # Crear instancia del extractor
        extractor = PDFExtractor(self.pdf_files)

        # Realizar la búsqueda
        self.search_results = extractor.search_terms(self.search_fields)

        # Cerrar el diálogo si se encontraron resultados
        if self.search_results:
            self.accept()
        else:
            # Mostrar mensaje si no se encontraron resultados
            msg = QLabel("No se encontraron resultados")
            msg.setStyleSheet(DIALOG_STYLES["message"])
            self.layout().addWidget(msg)

    def import_from_excel(self):
        dialog = ExcelImportDialog(self)
        if dialog.exec():
            for term in dialog.search_terms:
                self.add_confirmed_field(term)
            self.search_button.show()

    def add_confirmed_field(self, text):
        # Crear contenedor para el campo confirmado
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        # Flecha primero
        arrow = QLabel("➡️")
        arrow.setStyleSheet(DIALOG_STYLES["arrow_label"])
        layout.addWidget(arrow)

        # Texto del campo
        label = QLabel(text)
        label.setStyleSheet(DIALOG_STYLES["confirmed_item"])
        layout.addWidget(label)

        # Espacio flexible para empujar los botones a la derecha
        layout.addStretch()

        # Botón editar
        edit_button = QPushButton("Editar")
        edit_button.setStyleSheet(DIALOG_STYLES["edit_button"])
        edit_button.clicked.connect(lambda: self.edit_field(container, text))
        edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(edit_button)

        # Botón excluir
        exclude_button = QPushButton("Excluir")
        exclude_button.setStyleSheet(DIALOG_STYLES["exclude_button"])
        exclude_button.clicked.connect(lambda: self.exclude_field(container, text))
        exclude_button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(exclude_button)

        # Línea separadora
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(DIALOG_STYLES["separator_line"])

        # Añadir al layout principal
        self.fields_layout.insertWidget(0, separator)
        self.fields_layout.insertWidget(0, container)

        # Guardar el término de búsqueda
        self.search_fields[text] = text

        # Mostrar botón de búsqueda si hay al menos un campo
        self.search_button.show()

    def exclude_field(self, container, text):
        # Eliminar el término del diccionario
        self.search_fields.pop(text, None)

        # Obtener el índice del contenedor
        index = self.fields_layout.indexOf(container)

        # Eliminar el separador si existe
        if index > 0:  # Si hay un separador antes del campo
            separator = self.fields_layout.itemAt(index - 1).widget()
            separator.deleteLater()

        # Eliminar el contenedor
        container.deleteLater()

        # Ocultar el botón de búsqueda si no hay campos
        if not self.search_fields:
            self.search_button.hide()
