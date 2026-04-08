import re
import os
import base64
import urllib.request
import zlib
import shutil

# Konfiguration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENTRAL_IMAGE_DIR = os.path.join(BASE_DIR, 'docs', 'images')

if not os.path.exists(CENTRAL_IMAGE_DIR):
    os.makedirs(CENTRAL_IMAGE_DIR)

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
        print(f"  -> FEHLER bei API-Aufruf: {e}")
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

    # Bestimme lokalen Image-Ordner (relativ zur Datei)
    local_dir = os.path.dirname(file_path)
    local_image_dir = os.path.join(local_dir, 'images')
    if not os.path.exists(local_image_dir):
        os.makedirs(local_image_dir)

    new_content = content
    for i, code in enumerate(matches):
        file_basename = os.path.basename(file_path).replace('.md', '')
        # Eindeutiger Name für den zentralen Ordner
        safe_filename = file_basename.replace(' ', '_').lower()
        img_name = f"{safe_filename}_{i}.png"
        
        local_img_path = os.path.join(local_image_dir, img_name)
        central_img_path = os.path.join(CENTRAL_IMAGE_DIR, img_name)
        
        if generate_mermaid_image(code.strip(), local_img_path):
            print(f"  -> Bild generiert (Lokal): {img_name}")
            
            # Kopiere in den zentralen Ordner für Doxygen
            shutil.copy2(local_img_path, central_img_path)
            print(f"  -> Bild kopiert (Zentral): {img_name}")
            
            # Markdown-Link aktualisieren (relativ für lokale Vorschau)
            img_tag = f"![Diagramm](./images/{img_name})"
            if img_tag not in content:
                search_str = f"```mermaid\n{code}\n```"
                # Falls schon ein Link da ist, ersetzen wir den Block nicht doppelt
                if f"![Diagramm]" not in content:
                    new_content = new_content.replace(search_str, img_tag + "\n\n" + search_str)
        else:
            print(f"  -> FEHLER bei Bildgenerierung für {img_name}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    # Suche in Architektur und docs
    search_paths = [
        os.path.join(BASE_DIR, 'Architektur'),
        os.path.join(BASE_DIR, 'docs')
    ]
    
    for start_path in search_paths:
        if not os.path.exists(start_path): continue
        for root, dirs, files in os.walk(start_path):
            # doxygen_output ignorieren
            if 'doxygen_output' in root: continue
            
            for file in files:
                if file.endswith('.md'):
                    process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
