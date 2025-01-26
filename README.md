<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VOO-X PDF Extractor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            color: #333;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        pre {
            background: #f4f4f4;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            overflow-x: auto;
        }
        code {
            background: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 10px 0;
        }
        ul {
            margin-left: 20px;
        }
    </style>
</head>
<body>
    <h1>VOO-X PDF Extractor</h1>
    <p>Una aplicación de escritorio para extraer información específica de múltiples archivos PDF y exportarla a CSV.</p>

    <h2>Objetivo del Proyecto</h2>
    <p>Brindar una solución eficiente y amigable para la extracción masiva de datos de PDFs, permitiendo ahorrar tiempo y reducir errores en procesos manuales.</p>

    <h2>Características</h2>

    <h3>Interfaz Principal</h3>
    <ul>
        <li>Diseño moderno con título "VOO-X PDF EXTRACTOR".</li>
        <li>Menú superior con opciones de Archivo y Ayuda.</li>
        <li>Área central para selección de archivos.</li>
        <li>Barra de estado para mensajes informativos.</li>
        <li>Scroll vertical con diseño personalizado.</li>
    </ul>
    <img src="[URL_DE_LA_IMAGEN_MAIN_WINDOW]" alt="Interfaz Principal">

    <h3>Selección de Archivos</h3>
    <ul>
        <li>Botón "Seleccionar PDFs" para elegir archivos individuales.</li>
        <li>Botón "Seleccionar Carpeta" para procesar una carpeta completa.</li>
        <li>Visualización del número de archivos seleccionados.</li>
        <li>Soporte para múltiples archivos PDF.</li>
    </ul>

    <h3>Búsqueda en PDFs</h3>
    <ul>
        <li>Ventana dedicada para configurar términos de búsqueda.</li>
        <li>Dos métodos de entrada de términos:
            <ul>
                <li>Manual: Botón "Añadir Campo" para agregar términos uno a uno.</li>
                <li>Masivo: Importación desde archivo Excel (primera columna).</li>
            </ul>
        </li>
        <li>Edición y exclusión de términos de búsqueda.</li>
        <li>Interfaz con scroll para manejar múltiples términos.</li>
        <li>Separadores visuales entre términos.</li>
        <li>Confirmación de términos con tecla Enter o botón de confirmación.</li>
    </ul>
    <img src="[URL_DE_LA_IMAGEN_SEARCH_DIALOG]" alt="Diálogo de Búsqueda">

    <h3>Resultados</h3>
    <ul>
        <li>Ventana de resultados con tabla de datos extraídos.</li>
        <li>Columnas organizadas por términos de búsqueda.</li>
        <li>Botón "Exportar a CSV" para guardar resultados.</li>
        <li>Botón "Ver Tabla" para revisar últimos resultados.</li>
        <li>Soporte para maximizar/minimizar la ventana de resultados.</li>
    </ul>
    <img src="[URL_DE_LA_IMAGEN_RESULTS_WINDOW]" alt="Ventana de Resultados">

    <h3>Características Adicionales</h3>
    <ul>
        <li>Estilos personalizados con colores corporativos.</li>
        <li>Fuentes personalizadas para mejor legibilidad.</li>
        <li>Mensajes de error y confirmación.</li>
        <li>Interfaz responsiva y amigable.</li>
        <li>Soporte para archivos Excel (.xlsx, .xls) en importación masiva.</li>
    </ul>

    <h2>Requisitos</h2>
    <ul>
        <li>Python 3.x</li>
        <li>PySide6 (Qt para Python)</li>
        <li>pdfplumber</li>
        <li>pandas</li>
        <li>openpyxl</li>
    </ul>

    <h2>Instalación</h2>
    <ol>
        <li>Clonar el repositorio:
            <pre><code>git clone git@github.com:MouraAnalyst/pdf-extractor.git</code></pre>
        </li>
        <li>Instalar las dependencias:
            <pre><code>pip install PySide6 pdfplumber pandas openpyxl</code></pre>
        </li>
    </ol>

    <h2>Uso</h2>
    <ol>
        <li>Ejecutar la aplicación:
            <pre><code>python src/main.py</code></pre>
        </li>
        <li>Seleccionar archivos PDF usando los botones de la interfaz.</li>
        <li>Configurar términos de búsqueda (manual o masivamente desde Excel).</li>
        <li>Procesar los PDFs.</li>
        <li>Exportar resultados a CSV si se desea.</li>
    </ol>

    <h2>Estructura del Proyecto</h2>
    <pre><code>
src/
├── main.py                        # Punto de entrada de la aplicación
├── pdf_processor/                 # Módulo para procesamiento de PDFs
│   └── pdf_extractor.py           # Lógica de extracción de datos
└── ui/                            # Interfaz de usuario
    ├── main_window.py             # Ventana principal
    ├── styles/                    # Estilos de la aplicación
    │   └── style.py               # Definiciones de estilos
    └── dialogs/                   # Ventanas de diálogo
        ├── search_dialog.py       # Diálogo de búsqueda
        ├── results_dialog.py      # Diálogo de resultados
        └── excel_import_dialog.py # Diálogo de importación Excel
</code></pre>

    <h2>Pruebas</h2>
    <ol>
        <li>Asegúrese de que las dependencias están instaladas.</li>
        <li>Ejecute los tests ubicados en <code>tests_/</code>.</li>
        <li>Utilice los PDFs de prueba incluidos en <code>tests_/PDFs</code> para validar la funcionalidad.</li>
    </ol>

    <h2>Futuras Mejoras</h2>
    <ul>
        <li>Implementación de IA para mejorar la extracción de datos en PDFs basados en imágenes.</li>
        <li>Soporte para más formatos de archivo (e.g., JSON, XML).</li>
        <li>Función de previsualización de PDFs procesados.</li>
    </ul>

        <h2>Historial de Cambios</h2>
    <ul>
        <li><strong>Versión 1.1.0</strong>
            <ul>
                <li>Añadido soporte para añadir campos de forma masiva con archivo excel.</li>
                <li>Mejorada la interfaz gráfica.</li>
                <li>Corregidos errores en la exportación a CSV.</li>
            </ul>
        </li>
        <li><strong>Versión 1.0.0</strong>
            <ul>
                <li>Versión inicial con extracción de datos desde PDFs y exportación a CSV.</li>
            </ul>
        </li>
    </ul>

    <h2>Licencia</h2>
    <p>Este proyecto está licenciado bajo la Licencia MIT. Consulte el archivo LICENSE para más detalles.</p>

    <h2>Contribuciones</h2>
    <ol>
        <li>Haga un fork del repositorio.</li>
        <li>Cree una rama para su funcionalidad:
            <pre><code>git checkout -b feature/nueva-funcionalidad</code></pre>
        </li>
        <li>Haga un pull request con sus cambios.</li>
    </ol>
</body>
</html>