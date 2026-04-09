## @file init_db.py
#  @brief Initialisiert die Datenbankstrukturen für die Ingestion.
#
#  Dieses Skript erstellt die SQLite-Datenbank für den Staging-Bereich, 
#  definiert das Eingabe-Schema und lädt die notwendigen Stammdaten 
#  (wie Medikamentenkataloge) aus SQL-Skripten.
#
#  @date 2026-04-09

import sqlite3
import os

# Pfade definieren
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'database', 'blutdruck_input.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'database', 'input_schema.sql')
SEED_PATH = os.path.join(BASE_DIR, 'database', 'populate_master_data.sql')

def init_db():
    print(f"Initialisiere Datenbank unter: {DB_PATH}")
    
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Vorhandene Datenbank gelöscht.")
    
    # Verbindung herstellen
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Schema einlesen
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        cursor.executescript(schema_sql)
        print("Schema erfolgreich erstellt.")
        
        # Stammdaten einlesen
        with open(SEED_PATH, 'r', encoding='utf-8') as f:
            seed_sql = f.read()
        cursor.executescript(seed_sql)
        print("Stammdaten erfolgreich eingepflegt.")
        
        conn.commit()
    except Exception as e:
        print(f"Fehler bei der Initialisierung: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
