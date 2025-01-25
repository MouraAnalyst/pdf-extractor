import pdfplumber
import re
from typing import List, Dict, Any


class PDFExtractor:
    def __init__(self, pdf_files: List[str]):
        self.pdf_files = pdf_files

    def search_terms(self, search_fields: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Busca términos específicos en los archivos PDF.

        Args:
            search_fields: Diccionario con etiquetas y términos de búsqueda

        Returns:
            Lista de diccionarios con los resultados encontrados
        """
        results = []

        for pdf_file in self.pdf_files:
            try:
                with pdfplumber.open(pdf_file) as pdf:
                    # Extraer todo el texto del PDF
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text() or ""

                    # Buscar cada término
                    result = {"archivo": pdf_file}
                    found_any = False

                    for label, search_term in search_fields.items():
                        # Buscar el término exacto con posible contenido después
                        pattern = rf"{re.escape(search_term)}[:\s]+(.*?)(?:\n|$)"
                        matches = re.finditer(
                            pattern, text, re.IGNORECASE | re.MULTILINE
                        )

                        # Tomar la primera coincidencia
                        match = next(matches, None)

                        if match:
                            # Obtener el valor encontrado después del término
                            found_value = match.group(1).strip()
                            result[label] = found_value
                            found_any = True
                        else:
                            result[label] = "No encontrado"

                    if found_any:
                        results.append(result)

            except Exception as e:
                print(f"Error procesando {pdf_file}: {str(e)}")
                continue

        return results
