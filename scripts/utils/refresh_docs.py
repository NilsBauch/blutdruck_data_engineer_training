# ==============================================================================
# SCRIPT: refresh_docs.py
# BESCHREIBUNG: Zentrales Orchestrierungs-Skript für die Dokumentation.
#               Ruft die Bildmigration auf und bereitet alles für Doxygen vor.
# AUFRUF: py scripts/utils/refresh_docs.py (oder via update_docs.bat)
# ERGEBNIS: Aktualisierte Diagramm-Bilder und Vorbereitung für Doxygen.
# ==============================================================================

import os
import sys
import subprocess
import time

# --- KONFIGURATION & PFADE ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts', 'utils')
MIGRATE_SCRIPT = os.path.join(SCRIPTS_DIR, 'migrate_mermaid_to_images.py')

def main():
    print("="*60)
    print("DOKUMENTATIONS-REFRESH: START")
    print("="*60)
    
    start_time = time.time()
    
    # 1. Mermaid-Diagramme zu Bildern migrieren & synchronisieren
    print("\n[1/2] Generiere und synchronisiere Diagramme...")
    try:
        result = subprocess.run([sys.executable, MIGRATE_SCRIPT], 
                               cwd=BASE_DIR,
                               capture_output=True, 
                               text=True)
        if result.stdout:
            print(result.stdout.strip())
        if result.returncode != 0:
            print(f"FEHLER bei der Bildmigration:\n{result.stderr}")
            return
    except Exception as e:
        print(f"AUSNAHME bei der Bildmigration: {e}")
        return

    # 2. Hinweis auf Doxygen
    print("\n[2/2] Vorbereitung abgeschlossen.")
    print("-" * 60)
    print("Die Bilder wurden lokal und zentral (docs/images/) aktualisiert.")
    print("Du kannst nun 'doxygen' in deinem Terminal ausführen, um die HTML-Doku zu erstellen.")
    print("-" * 60)
    
    duration = time.time() - start_time
    print(f"\nREFRESH ERFOLGREICH BEENDET (Dauer: {duration:.2f}s).")
    print("="*60)

if __name__ == "__main__":
    main()
