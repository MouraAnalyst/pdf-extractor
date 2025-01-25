from PySide6.QtGui import QFont

# Colores
COLORS = {
    "primary": "#0d47a1",  # Azul oscuro
    "secondary": "#f5f5f5",  # Blanco gelo
    "accent": "#304ffe",  # Azul acento
    "text": "#2c3e50",  # Color texto principal
    "button_text": "#ffffff",  # Texto botones
    "border": "#0d47a1",  # Azul oscuro para bordes
    "title_text": "#666666",  # Gris claro para el título
}

# Estilos CSS
STYLES = {
    "main_window": f"""
        QMainWindow {{
            background-color: {COLORS['secondary']};
            border: 10px solid {COLORS['border']};
        }}
    """,
    "menubar": f"""
        QMenuBar {{
            background-color: {COLORS['border']};
            color: {COLORS['button_text']};
            border-bottom: 2px solid {COLORS['border']};
            padding: 5px;
            font-family: "Courier New";
            font-weight: bold;
        }}
        QMenuBar::item {{
            background-color: transparent;
            padding: 5px 10px;
            margin: 0px 2px;
            color: {COLORS['button_text']};
            font-family: "Courier New";
            font-weight: bold;
        }}
        QMenuBar::item:selected {{
            background-color: {COLORS['accent']};
            border-radius: 4px;
        }}
        QMenu {{
            background-color: {COLORS['secondary']};
            font-family: "Courier New";
            font-size: 14px;
            font-weight: bold;
        }}
        QMenu::item {{
            padding: 5px 20px;
            color: {COLORS['text']};
        }}
        QMenu::item:selected {{
            background-color: {COLORS['accent']};
            color: {COLORS['button_text']};
        }}
    """,
    "title_voo": f"""
        QLabel {{
            color: {COLORS['title_text']};
            font-family: Impact;
            font-size: 32px;
            padding: 10px 30px 0px 30px;
            margin: 10px 20px 0px 20px;
            background: transparent;
            font-weight: bold;
        }}
    """,
    "title_pdf": f"""
        QLabel {{
            color: {COLORS['title_text']};
            font-family: Impact;
            font-size: 64px;
            padding: 0px 30px 30px 30px;
            margin: 0px 20px 20px 20px;
            background: transparent;
            font-weight: bold;
        }}
    """,
    "instruction_label": f"""
        QLabel {{
            color: {COLORS['text']};
            font-family: "Courier New";
            font-size: 20px;
            margin: 20px;
            padding: 15px;
            background-color: rgba(255,255,255,0.9);
            border-radius: 10px;
            font-weight: bold;
        }}
    """,
    "button": f"""
        QPushButton {{
            background-color: {COLORS['primary']};
            color: {COLORS['button_text']};
            font-family: "Courier New";
            border-radius: 15px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            margin: 10px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['accent']};
        }}
        QPushButton:pressed {{
            background-color: {COLORS['primary']};
            padding: 9px 19px;
        }}
    """,
    "central_widget": f"""
        QWidget {{
            background-color: {COLORS['secondary']};
            border-radius: 15px;
            margin: 10px;
        }}
    """,
    "statusbar": f"""
        QStatusBar {{
            padding: 20px 50px;
            margin: 25px 50px 25px 50px;
            color: {COLORS['text']};
            font-family: "Courier New";
            font-size: 24px;
            font-weight: bold;
        }}
    """,
    "info_label": f"""
        QLabel {{
            color: {COLORS['text']};
            font-family: "Courier New";
            font-size: 16px;
            padding: 10px;
            background-color: rgba(255,255,255,0.9);
            border-radius: 10px;
            font-weight: bold;
            margin: 5px 10px;
        }}
    """,
    "process_button": f"""
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
        QPushButton:pressed {{
            background-color: {COLORS['accent']};
            padding: 9px 19px;
        }}
    """,
    "progress_area": f"""
        QLabel {{
            color: {COLORS['text']};
            font-family: "Courier New";
            font-size: 16px;
            padding: 20px;
            background-color: white;
            border-radius: 10px;
            border: 2px solid {COLORS['border']};
            margin: 10px 20px;
        }}
    """,
}

# Fuentes
FONTS = {
    "title_voo": QFont("Impact", 32, QFont.Weight.Bold),
    "title_pdf": QFont("Impact", 64, QFont.Weight.Bold),
    "normal": QFont("Courier New", 18, QFont.Weight.Bold),
    "button": QFont("Courier New", 16, QFont.Weight.Bold),
}
