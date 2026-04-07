import csv
import json
import sqlite3
import os
import re
from datetime import datetime

# Pfade
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', '01_raw')
DB_PATH = os.path.join(BASE_DIR, 'database', 'blutdruck_input.db')

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def format_timestamp_to_iso(date_str, time_str):
    """Konvertiert DD.MM.YYYY und HH:MM zu YYYY-MM-DD HH:MM:SS"""
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", '%d.%m.%Y %H:%M')
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return None

def load_blood_pressure(user_id, patient_folder):
    csv_dir = os.path.join(RAW_DATA_DIR, patient_folder, 'csv')
    if not os.path.exists(csv_dir):
        print(f"[BP] Verzeichnis nicht gefunden: {csv_dir}")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    
    count = 0
    for filename in os.listdir(csv_dir):
        if filename.endswith('.csv'):
            path = os.path.join(csv_dir, filename)
            print(f"[BP] Lade {filename}...")
            with open(path, mode='r', encoding='utf-8') as f:
                lines = f.readlines()
                data_start = False
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('Datum;Uhrzeit'):
                        if line.startswith('Datum;Uhrzeit'): data_start = True
                        continue
                    
                    if data_start:
                        parts = line.split(';')
                        if len(parts) >= 5:
                            ts = format_timestamp_to_iso(parts[0], parts[1])
                            if ts:
                                cursor.execute('''
                                    INSERT INTO raw_blood_pressure (user_id, timestamp, systolic, diastolic, pulse, is_manual)
                                    VALUES (?, ?, ?, ?, ?, ?)
                                ''', (user_id, ts, int(parts[2]), int(parts[3]), int(parts[4]), int(parts[6])))
                                count += 1
    
    conn.commit()
    conn.close()
    print(f"[BP] {count} Einträge für User {user_id} geladen.")

def load_activity_data(user_id, patient_folder):
    activity_dir = os.path.join(RAW_DATA_DIR, patient_folder, 'json', 'Takeout', 'Google Fit', 'Tägliche Aktivitätswerte')
    if not os.path.exists(activity_dir):
        print(f"[Activity] Verzeichnis nicht gefunden: {activity_dir}")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    
    count = 0
    for filename in os.listdir(activity_dir):
        if re.match(r'\d{4}-\d{2}-\d{2}\.csv', filename):
            day = filename.replace('.csv', '')
            path = os.path.join(activity_dir, filename)
            
            day_steps = 0
            day_weight = None
            day_active_mins = 0
            
            with open(path, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                
                try:
                    idx_steps = header.index('Schrittzahl')
                    idx_weight = header.index('Durchschnittsgewicht (kg)')
                    idx_active = header.index('Anzahl der Aktivitätsminuten')
                except ValueError:
                    continue

                for row in reader:
                    if not row: continue
                    if row[idx_steps]:
                        day_steps += int(float(row[idx_steps]))
                    if row[idx_weight] and day_weight is None: # Ersten validen Wert nehmen
                        day_weight = float(row[idx_weight].replace(',', '.'))
                    if row[idx_active]:
                        day_active_mins += int(float(row[idx_active]))

            cursor.execute('''
                INSERT INTO raw_activity_daily (user_id, date, steps, activity_minutes, weight_kg)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, day, day_steps, day_active_mins, day_weight))
            count += 1
    
    conn.commit()
    conn.close()
    print(f"[Activity] {count} Tage für User {user_id} geladen.")

def main():
    print(f"=== ETL-PROZESS START ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Alle registrierten Nutzer und deren Verzeichnisse abrufen
    try:
        cursor.execute("SELECT user_id, name, raw_data_folder FROM master_lifestyle")
        users = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Fehler beim Abrufen der Nutzer-Metadaten: {e}")
        conn.close()
        return

    if not users:
        print("Keine Nutzer mit Verzeichnis-Metadaten in master_lifestyle gefunden.")
    
    for user_id, name, raw_folder in users:
        if not raw_folder:
            print(f"Skipping User {user_id} ({name}): Kein raw_data_folder hinterlegt.")
            continue
            
        print(f"\n--- Verarbeite Nutzer: {name} (ID: {user_id}, Ordner: {raw_folder}) ---")
        
        # Staging: Daten für diesen Nutzer zurücksetzen
        cursor.execute("DELETE FROM raw_blood_pressure WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM raw_activity_daily WHERE user_id = ?", (user_id,))
        conn.commit()
        
        # 1. Blutdruck (SVD)
        load_blood_pressure(user_id, raw_folder)
        
        # 2. Smartwatch (Schritte, Gewicht, Aktivität)
        load_activity_data(user_id, raw_folder)
        
    conn.close()
    print("\n=== ETL-PROZESS BEENDET ===")

if __name__ == "__main__":
    main()
