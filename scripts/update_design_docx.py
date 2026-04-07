import os
import re
import zlib
import base64
import urllib.request
import subprocess

# Pfade
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD_FILE = os.path.join(BASE_DIR, 'Architektur', 'Design', 'Design_Dokumentation.md')
IMAGE_DIR = os.path.join(BASE_DIR, 'Architektur', 'images')
MD_TO_DOCX_SCRIPT = os.path.join(BASE_DIR, 'scripts', 'md_to_docx.py')

def generate_kroki_image(mermaid_code, output_path):
    """Nutzt die Kroki-API, um Mermaid-Code in ein PNG zu verwandeln."""
    try:
        # Kroki-Format: zlib-komprimiert -> Base64 url-safe
        payload = base64.urlsafe_b64encode(zlib.compress(mermaid_code.encode('utf-8'), 9)).decode('ascii')
        url = f"https://kroki.io/mermaid/png/{payload}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        print(f"  -> {os.path.basename(output_path)} aktualisiert.")
        return True
    except Exception as e:
        print(f"  -> Fehler bei {os.path.basename(output_path)}: {e}")
        return False

def main():
    print("=== Master-Update: Design-Dokumentation (PNG & DOCX) ===")
    
    if not os.path.exists(MD_FILE):
        print(f"Fehler: {MD_FILE} nicht gefunden.")
        return

    with open(MD_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. ERM (Business-DB) extrahieren
    print("Extrahiere Diagramme aus Markdown...")
    erm_match = re.search(r'### ERM \(Business-DB\)\s*?\n```mermaid\n(.*?)\n```', content, re.DOTALL)
    if erm_match:
        generate_kroki_image(erm_match.group(1).strip(), os.path.join(IMAGE_DIR, 'design_erm_business.png'))
    else:
        print("  -> Hinweis: Sektion '### ERM (Business-DB)' mit Mermaid-Block nicht gefunden.")

    # 2. mER (Star-Schema) extrahieren
    mer_match = re.search(r'### mER \(Star-Schema\)\s*?\n```mermaid\n(.*?)\n```', content, re.DOTALL)
    if mer_match:
        generate_kroki_image(mer_match.group(1).strip(), os.path.join(IMAGE_DIR, 'design_mer_dwh.png'))
    else:
        print("  -> Hinweis: Sektion '### mER (Star-Schema)' mit Mermaid-Block nicht gefunden.")

    # 3. DOCX neu generieren
    print("Generiere finalem Word-Dokument...")
    try:
        # Wir nutzen 'py', da dies auf Windows der Standard-Wrapper ist
        subprocess.run(['py', MD_TO_DOCX_SCRIPT], check=True)
        print("=== Erfolg: Alle Dateien aktuell! ===")
    except Exception as e:
        print(f"Fehler beim Aufruf von md_to_docx.py: {e}")

if __name__ == "__main__":
    main()
