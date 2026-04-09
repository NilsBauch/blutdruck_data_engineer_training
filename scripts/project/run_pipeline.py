## @file run_pipeline.py
#  @brief Zentrale Orchestrierung der Health-Data-Pipeline.
#
#  Dieses Skript steuert den gesamten Prozess von der Datenbank-Initialisierung 
#  über die Datengenerierung bis hin zur Transformation in das Data Warehouse.
#
#  @section Workflow Vorgehensweise
#  1. **Initialisierung**: Datenbanken werden zurückgesetzt und Stammdaten geladen.
#  2. **Loading**: Die Rohdaten werden in die Staging-Datenbank geladen.
#  3. **Transformation**: Die Daten werden in das Star-Schema (DWH) überführt.
#
#  @date 2026-04-08

import os
import sys
import subprocess
import time

# Pfade zu den Unterordnern definieren (relativ zu diesem Skript)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts", "project")
ETL_DIR = os.path.join(BASE_DIR, "etl")

# Liste der Skripte in der richtigen Reihenfolge
PIPELINE_STEPS = [
    {
        "name": "DB-Initialisierung",
        "path": os.path.join(SCRIPTS_DIR, "init_db.py"),
        "description": "Erstellt die Eingabe-Datenbank und lädt Medikamente-Stammdaten."
    },
    {
        "name": "Rohdaten-Laden (Extract & Load)",
        "path": os.path.join(SCRIPTS_DIR, "load_raw_data.py"),
        "description": "Liest die vorhandenen Dateien aus 'data/01_raw' in die Datenbank ein."
    },
    {
        "name": "DWH-Transformation (Transform)",
        "path": os.path.join(SCRIPTS_DIR, "build_dwh.py"),
        "description": "Überführt die geladenen Daten in das Star-Schema (blutdruck_dwh.db)."
    }
]

def run_step(step_index, step_info):
    """Führt einen einzelnen Schritt der Pipeline aus."""
    name = step_info["name"]
    script_path = step_info["path"]
    
    print(f"\n" + "="*60)
    print(f"SCHRITT {step_index + 1}: {name}")
    print(f"Beschreibung: {step_info['description']}")
    print("-" * 60)
    
    start_time = time.time()
    
    try:
        # Wir nutzen sys.executable, um denselben Python-Interpreter zu verwenden
        # Das ist stabiler als nur 'python' oder 'py' zu tippen.
        result = subprocess.run([sys.executable, script_path], 
                               cwd=BASE_DIR,
                               capture_output=True, 
                               text=True)
        
        # Output des Skripts anzeigen
        if result.stdout:
            print(result.stdout.strip())
            
        if result.returncode != 0:
            print(f"\n[FEHLER] Schritt '{name}' ist fehlgeschlagen!")
            if result.stderr:
                print(f"Fehlermeldung:\n{result.stderr}")
            return False
            
        end_time = time.time()
        print(f"-> Erfolg! (Dauer: {end_time - start_time:.2f} Sekunden)")
        return True
        
    except Exception as e:
        print(f"\n[EXCEPTION] Unerwarteter Fehler in '{name}': {e}")
        return False

def main():
    """Hauptfunktion zur Steuerung der Pipeline."""
    print("*"*60)
    print("STARTE GESAMT-PIPELINE (END-TO-END)")
    print("*"*60)
    
    start_all = time.time()
    all_success = True
    
    for i, step in enumerate(PIPELINE_STEPS):
        if not run_step(i, step):
            all_success = False
            break # Bei Fehler stoppen wir die Kette
            
    print("\n" + "*"*60)
    if all_success:
        duration = time.time() - start_all
        print(f"PIPELINE ERFOLGREICH BEENDET.")
        print(f"Gesamtdauer: {duration:.2f} Sekunden")
        print(f"Daten stehen nun in 'database/blutdruck_dwh.db' bereit.")
    else:
        print("PIPELINE ABGEBROCHEN. Bitte Fehler oben prüfen.")
    print("*"*60)

if __name__ == "__main__":
    main()
