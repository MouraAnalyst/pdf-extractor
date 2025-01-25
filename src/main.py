# src/main.py
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # Verificar fuentes disponibles
    print("Fuentes disponibles:")
    for family in QFontDatabase().families():
        print(family)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
