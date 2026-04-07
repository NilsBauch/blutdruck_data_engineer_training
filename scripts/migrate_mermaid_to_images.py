import re
import os
import base64
import urllib.request
import urllib.error

# Konfiguration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, 'Architektur', 'images')
SEARCH_DIR = os.path.join(BASE_DIR, 'Architektur')

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

import zlib

def generate_mermaid_image(mermaid_code, output_path):
    """Konvertiert Mermaid-Code via Kroki API in ein PNG-Bild."""
    try:
        # Kroki Encoding: UTF-8 -> zlib compress -> base64 urlsafe
        payload = base64.urlsafe_b64encode(zlib.compress(mermaid_code.encode('utf-8'), 9)).decode('ascii')
        url = f"https://kroki.io/mermaid/png/{payload}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.read())
                return True
    except Exception as e:
        print(f"  -> FEHLER: {e}")
    return False

def process_file(file_path):
    print(f"Verarbeite: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find mermaid blocks: ```mermaid ... ```
    pattern = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)
    matches = pattern.findall(content)
    
    if not matches:
        return

    new_content = content
    for i, code in enumerate(matches):
        file_basename = os.path.basename(file_path).replace('.md', '')
        img_name = f"{file_basename}_{i}.png"
        img_path = os.path.join(IMAGE_DIR, img_name)
        
        # Falls es sich um die Design_Dokumentation handelt, nutzen wir die festen Namen
        if "Design_Dokumentation" in file_basename:
            if "ERM (Business-DB)" in content[:content.find(code)]:
                img_name = "design_erm_business.png"
            elif "mER (Star-Schema)" in content[:content.find(code)]:
                img_name = "design_mer_dwh.png"
            img_path = os.path.join(IMAGE_DIR, img_name)

        if generate_mermaid_image(code.strip(), img_path):
            print(f"  -> Bild aktualisiert: {img_name}")
            # Nur Tag einfügen, wenn kein Bild-Link direkt davor oder danach ist
            img_tag = f"![Diagramm](./images/{img_name})"
            if img_name not in content:
                # Einfaches Einfügen über dem Block
                search_str = f"```mermaid\n{code}\n```"
                new_content = new_content.replace(search_str, img_tag + "\n\n" + search_str)
        else:
            print(f"  -> FEHLER bei Bildgenerierung für {img_name}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    # Alle .md Dateien in Architektur (rekursiv)
    for root, dirs, files in os.walk(SEARCH_DIR):
        for file in files:
            if file.endswith('.md'):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
