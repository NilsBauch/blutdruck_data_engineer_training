# ==============================================================================
# SCRIPT: check_counts.py
# BESCHREIBUNG: Gibt eine schnelle Übersicht über die Zeilenanzahlen aller Tabellen
#               in beiden Datenbanken (Staging & Data Warehouse).
# AUFRUF: py scripts/utils/check_counts.py
# ERGEBNIS: Konsolenausgabe mit Tabellennamen und deren Datensatz-Anzahl.
# ==============================================================================

import sqlite3
import os

# Pfad zum Projekt-Hauptverzeichnis (3 Ebenen nach oben von scripts/utils/ aus)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_db(db_name):
    """Prüft eine SQLite-Datenbank und listet alle Tabellen mit Zeilenanzahl auf."""
    
    # Vollständiger Pfad zur Datenbank-Datei
    path = os.path.join(BASE_DIR, 'database', db_name)
    
    # Sicherheitsprüfung: Existiert die Datei?
    if not os.path.exists(path):
        print(f"\nHINWEIS: Datenbank '{db_name}' wurde noch nicht erstellt.")
        return
    
    # Verbindung zur Datenbank herstellen
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    
    print(f"\nTabellen-Übersicht für: {db_name}")
    print("-" * 40)
    
    try:
        # 1. Namen aller Tabellen aus dem System-Schema abrufen
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        # 2. Für jede Tabelle die Anzahl der Zeilen zählen
        for (table_name,) in tables:
            # Vorsicht: Bei dynamischen Tabellennamen keine Platzhalter verwenden (?) sondern f-strings, 
            # da Tabellennamen keine Variablenwerte im SQL-Sinne sind.
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  - {table_name:<20}: {count:>5} Datensätze")
            
    except Exception as e:
        print(f"  [FEHLER] Konnte Daten nicht lesen: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Wir prüfen beide Datenbanken des Projekts
    check_db('blutdruck_input.db')  # Der Eingabebereich (Staging)
    check_db('blutdruck_dwh.db')    # Das fertige Data Warehouse

