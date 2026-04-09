# ==============================================================================
# SCRIPT: migrate_mermaid_to_images.py
# BESCHREIBUNG: Sucht in allen Markdown-Dateien nach Mermaid-Diagrammen und 
#               konvertiert diese via Kroki-API in PNG-Bilder.
# AUFRUF: py scripts/utils/migrate_mermaid_to_images.py
# ERGEBNIS: PNG-Bilder in lokalen 'images/'-Ordnern und unter 'docs/images/'.
# ==============================================================================

import re
import os
import base64
import urllib.request
import zlib
import shutil

# --- KONFIGURATION & PFADE ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

    # Bestimme lokalen Image-Ordner (IMMER Unterordner 'images' der aktuellen Datei)
    local_dir = os.path.dirname(file_path)
    local_image_target_dir = os.path.join(local_dir, 'images')
    if not os.path.exists(local_image_target_dir):
        os.makedirs(local_image_target_dir)

    new_content = content
    # Wir entfernen zuerst alle alten, möglicherweise kaputten Bild-Links, die das Skript vorher eingefügt hat
    new_content = re.sub(r'!\[Diagramm\]\(.*?\)\n\n', '', new_content)
    # Entferne auch spezifische Architektur-Links, die wir vorher falsch gesetzt haben
    new_content = re.sub(r'!\[Aktivitätsdiagramm.*?\]\(.*?\)\n\n', '', new_content)

    for i, code in enumerate(matches):
        file_basename = os.path.basename(file_path).replace('.md', '')
        safe_filename = file_basename.replace(' ', '_').lower()
        img_name = f"{safe_filename}_{i}.png"
        
        local_img_path = os.path.join(local_image_target_dir, img_name)
        central_img_path = os.path.join(CENTRAL_IMAGE_DIR, img_name)
        
        if generate_mermaid_image(code.strip(), local_img_path):
            print(f"  -> Bild generiert (Lokal): {img_name}")
            
            # Kopiere in den zentralen Ordner für Doxygen
            shutil.copy2(local_img_path, central_img_path)
            
            # Link setzen: images/filename.png (Funktioniert lokal in VS Code und in Doxygen via IMAGE_PATH)
            img_tag = f"![Diagramm](images/{img_name})"
            search_str = f"```mermaid\n{code}\n```"
            new_content = new_content.replace(search_str, img_tag + "\n\n" + search_str)
        else:
            print(f"  -> FEHLER bei Bildgenerierung für {img_name}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    search_paths = [
        os.path.join(BASE_DIR, 'Architektur'),
        os.path.join(BASE_DIR, 'docs')
    ]
    
    for start_path in search_paths:
        if not os.path.exists(start_path): continue
        for root, dirs, files in os.walk(start_path):
            if 'doxygen_output' in root: continue
            if 'images' in dirs: dirs.remove('images') # Nicht in images-Ordnern suchen
            
            for file in files:
                if file.endswith('.md'):
                    process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
