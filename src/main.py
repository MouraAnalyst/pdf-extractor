# src/main.py
import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    # Forzar el uso de X11
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    os.environ["XDG_SESSION_TYPE"] = "x11"

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
