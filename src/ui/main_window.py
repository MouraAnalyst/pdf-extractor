# src/ui/main_window.py
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QMenuBar,
    QMenu,
    QStatusBar,
    QPushButton,
    QHBoxLayout,
    QStackedLayout,
    QFileDialog,
    QScrollArea,
    QDialog,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QAction
from ui.styles.style import STYLES, FONTS, COLORS
import os
from ui.dialogs.search_dialog import SearchDialog
from ui.dialogs.results_dialog import ResultsDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voo-X PDF Extractor")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(STYLES["main_window"])
        self.last_results = None  # Almacenar últimos resultados

        # Configurar el widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.central_widget.setStyleSheet(STYLES["central_widget"])

        # Crear el menú
        self.create_menu()

        # Crear el título
        self.create_title()

        # Crear la barra de estado
        self.statusBar = QStatusBar()
        self.statusBar.setFont(FONTS["normal"])
        self.statusBar.setStyleSheet(STYLES["statusbar"])
        self.setStatusBar(self.statusBar)

        # Configurar la interfaz principal
        self.setup_ui()

        # Crear un widget scrollable
        scroll = QScrollArea()
        scroll.setWidget(self.central_widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
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
        self.setCentralWidget(scroll)

    def create_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet(STYLES["menubar"])

        # Menú Archivo
        file_menu = menubar.addMenu("Archivo")

        # Acciones del menú archivo
        open_action = QAction("Abrir PDF", self)
        open_action.triggered.connect(self.open_pdf)

        open_folder_action = QAction("Abrir Carpeta", self)
        open_folder_action.triggered.connect(self.open_folder)

        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(open_action)
        file_menu.addAction(open_folder_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Menú Ayuda
        help_menu = menubar.addMenu("Ayuda")
        about_action = QAction("Acerca de", self)
        help_menu.addAction(about_action)

    def create_title(self):
        # Contenedor para el título
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setSpacing(0)

        # VOO-X
        voo_label = QLabel("VOO-X")
        voo_label.setFont(FONTS["title_voo"])
        voo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        voo_label.setStyleSheet(STYLES["title_voo"])
        title_layout.addWidget(voo_label)

        # PDF EXTRACTOR
        pdf_label = QLabel("PDF EXTRACTOR")
        pdf_label.setFont(FONTS["title_pdf"])
        pdf_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pdf_label.setStyleSheet(STYLES["title_pdf"])
        title_layout.addWidget(pdf_label)

        self.layout.addWidget(title_container)

    def setup_ui(self):
        # Instrucciones
        instruction_label = QLabel("Seleccione la carpeta o archivos PDF para comenzar")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_label.setFont(FONTS["normal"])
        instruction_label.setStyleSheet(STYLES["instruction_label"])
        self.layout.addWidget(instruction_label)

        # Contenedor horizontal para botones
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(20)

        # Botones de selección
        select_files_btn = QPushButton("Seleccionar PDFs")
        select_files_btn.setFont(FONTS["button"])
        select_files_btn.setStyleSheet(STYLES["button"])
        select_files_btn.clicked.connect(self.open_pdf)
        button_layout.addWidget(select_files_btn)

        select_folder_btn = QPushButton("Seleccionar Carpeta")
        select_folder_btn.setFont(FONTS["button"])
        select_folder_btn.setStyleSheet(STYLES["button"])
        select_folder_btn.clicked.connect(self.open_folder)
        button_layout.addWidget(select_folder_btn)

        self.layout.addWidget(button_container)

        # Área de información de archivos seleccionados
        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setFont(FONTS["normal"])
        self.info_label.setStyleSheet(STYLES["info_label"])
        self.info_label.hide()
        self.layout.addWidget(self.info_label)

        # Contenedor para botones de proceso
        process_buttons = QWidget()
        process_layout = QHBoxLayout(process_buttons)
        process_layout.setSpacing(10)
        process_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botón procesar
        self.process_button = QPushButton("Procesar PDFs")
        self.process_button.setFont(FONTS["button"])
        self.process_button.setStyleSheet(STYLES["process_button"])
        self.process_button.clicked.connect(self.process_pdfs)
        self.process_button.hide()
        process_layout.addWidget(self.process_button)

        # Botón ver última tabla
        self.show_last_results_button = QPushButton("Ver Tabla")
        self.show_last_results_button.setFont(FONTS["button"])
        self.show_last_results_button.setStyleSheet(STYLES["process_button"])
        self.show_last_results_button.clicked.connect(self.show_last_results)
        self.show_last_results_button.hide()
        process_layout.addWidget(self.show_last_results_button)

        self.layout.addWidget(process_buttons)

        # Área de progreso
        self.progress_label = QLabel("")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setFont(FONTS["normal"])
        self.progress_label.setStyleSheet(STYLES["progress_area"])
        self.progress_label.hide()
        self.layout.addWidget(self.progress_label)

        self.layout.addStretch()

    def open_pdf(self):
        default_path = "/mnt/c/Users"  # Ruta por defecto

        file_dialog = QFileDialog(self)
        file_dialog.setDirectory(default_path)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("Archivos PDF (*.pdf)")
        file_dialog.setViewMode(QFileDialog.ViewMode.List)
        file_dialog.setWindowTitle("Seleccionar archivos PDF")

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                num_files = len(selected_files)
                self.info_label.setText(
                    f"✓ {num_files} archivo{'s' if num_files > 1 else ''} PDF seleccionado{'s' if num_files > 1 else ''}"
                )
                self.info_label.show()
                self.selected_pdf_files = selected_files
                self.process_button.show()  # Mostrar el botón de procesamiento
                self.progress_label.hide()  # Ocultar el área de progreso

    def open_folder(self):
        default_path = "/mnt/c/Users"  # Ruta por defecto

        folder_dialog = QFileDialog(self)
        folder_dialog.setDirectory(default_path)
        folder_dialog.setFileMode(QFileDialog.FileMode.Directory)
        folder_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        folder_dialog.setWindowTitle("Seleccionar Carpeta con PDFs")

        if folder_dialog.exec():
            selected_folder = folder_dialog.selectedFiles()[0]
            pdf_files = [
                os.path.join(selected_folder, f)
                for f in os.listdir(selected_folder)
                if f.lower().endswith(".pdf")
            ]

            if pdf_files:
                num_files = len(pdf_files)
                self.info_label.setText(
                    f"✓ {num_files} archivo{'s' if num_files > 1 else ''} PDF encontrado{'s' if num_files > 1 else ''}"
                )
                self.info_label.show()
                self.selected_pdf_files = pdf_files
                self.process_button.show()  # Mostrar el botón de procesamiento
                self.progress_label.hide()  # Ocultar el área de progreso
            else:
                self.info_label.setText(
                    "❌ No se encontraron archivos PDF en la carpeta seleccionada"
                )
                self.info_label.show()
                self.process_button.hide()  # Ocultar el botón de procesamiento
                self.progress_label.hide()  # Ocultar el área de progreso

    def process_pdfs(self):
        """Función que se llamará cuando se presione el botón de procesar"""
        # Abrir el diálogo de búsqueda
        dialog = SearchDialog(self, pdf_files=self.selected_pdf_files)

        # Si el usuario completó la búsqueda y hay resultados
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.search_results:
            self.last_results = dialog.search_results  # Guardar resultados
            # Mostrar los resultados en la nueva ventana
            results_dialog = ResultsDialog(self, results=dialog.search_results)
            results_dialog.exec()
            # Mostrar el botón de ver última tabla
            self.show_last_results_button.show()

    def show_last_results(self):
        """Muestra la última tabla de resultados generada"""
        if self.last_results:
            results_dialog = ResultsDialog(self, results=self.last_results)
            results_dialog.exec()
