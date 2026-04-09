# ==============================================================================
# SCRIPT: render_mermaid.py
# BESCHREIBUNG: Ein eigenständiges Werkzeug, um Mermaid-Diagramm-Code (Text)
#               über die Kroki-API in ein Bild (PNG) zu konvertieren.
# AUFRUF: Kann als Modul importiert oder direkt angepasst werden.
# ERGEBNIS: Speichert ein PNG-Bild des übergebenen Diagramms.
# ==============================================================================

import base64
import requests
import os

# ==============================================================================
# FUNKTION: generate_mermaid_image
# VERWENDUNG:
# Um ein individuelles Diagramm zu generieren, rufen Sie die Funktion mit dem
# Mermaid-String und dem gewünschten Dateipfad auf:
#
#   code = "graph TD; A-->B;"
#   generate_mermaid_image(code, "diagramm.png")
# ==============================================================================

def generate_mermaid_image(mermaid_code, output_path):
    """Konvertiert Mermaid-Code via mermaid.ink API in ein PNG-Bild."""
    print(f"Generiere Bild für {output_path}...")
    
    # Mermaid-Code in Base64 konvertieren (UTF-8 safe)
    code_bytes = mermaid_code.encode('utf-8')
    base64_code = base64.b64encode(code_bytes).decode('utf-8')
    
    # API URL (wir nutzen die .ink API, die sehr zuverlässig ist)
    url = f"https://mermaid.ink/img/{base64_code}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Erfolg: Bild gespeichert unter {output_path}")
            return True
        else:
            print(f"Fehler: API antwortete mit Status {response.status_code}")
            return False
    except Exception as e:
        print(f"Ausnahme bei API-Abfrage: {e}")
        return False

# Beispielhafte Ausführung für das erste Diagramm
if __name__ == "__main__":
    code = """
flowchart TD
    A[Start] --> B[Ende]
    """
    # Test-Pfad
    # generate_mermaid_image(code, "test_mermaid.png")
