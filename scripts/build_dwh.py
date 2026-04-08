## @file build_dwh.py
#  @brief Transformations-Skript für das Data Warehouse (Star-Schema).
#
#  Dieses Skript überführt die Daten aus der Staging-Datenbank in das 
#  analytische Star-Schema. Es implementiert eine **SCD Type 2 Historisierung** 
#  für Dimensionen und eine inkrementelle Beladung der Faktentabelle.
#
#  @date 2026-04-08

import sqlite3
import os
from datetime import datetime, timedelta

# Pfade
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DB = os.path.join(BASE_DIR, 'database', 'blutdruck_input.db')
DWH_DB = os.path.join(BASE_DIR, 'database', 'blutdruck_dwh.db')
SCHEMA_SQL = os.path.join(BASE_DIR, 'database', 'dwh_schema.sql')

## @brief Initialisiert das DWH-Schema, falls es noch nicht existiert.
def init_dwh():
    print("Initialisiere DWH Schema (IF NOT EXISTS)...")
    
    conn = sqlite3.connect(DWH_DB)
    with open(SCHEMA_SQL, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()

## @brief Migriert Patienten-, Medikations- und Zeitdaten in die Dimensionstabellen.
#  
#  Verwendet für Medikation und Lifestyle eine **SCD Type 2** Logik:
#  - Falls sich ein Attribut ändert, wird der alte Datensatz geschlossen (SCD_valid_to = JETZT).
#  - Ein neuer Datensatz mit dem neuen Wert wird geöffnet (SCD_valid_to = 9999-12-31).
def migrate_dimensions():
    print("Migriere Dimensionen (SCD Type 2)...")
    in_conn = sqlite3.connect(INPUT_DB)
    out_conn = sqlite3.connect(DWH_DB)
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # --- dim_user (Stammdaten, einfacher Overwrite/Insert) ---
    users = in_conn.execute("SELECT user_id, gender, age FROM master_lifestyle").fetchall()
    for uid, gen, age in users:
        out_conn.execute('''
            INSERT INTO dim_user (user_id, gender, age) VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET gender=excluded.gender, age=excluded.age
        ''', (uid, gen, age))
    
    # --- dim_medication (SCD Type 2) ---
    meds = in_conn.execute("SELECT med_id, name, dose_mg, description FROM master_medications").fetchall()
    for mid, name, dose, cat in meds:
        # Prüfen, ob eine aktive Version existiert
        current = out_conn.execute('''
            SELECT med_key, name, dosage_mg, category FROM dim_medication 
            WHERE med_id = ? AND SCD_valid_to = '9999-12-31'
        ''', (mid,)).fetchone()
        
        if not current:
            # Neu anlegen
            out_conn.execute('''
                INSERT INTO dim_medication (med_id, name, dosage_mg, category, SCD_valid_from)
                VALUES (?, ?, ?, ?, ?)
            ''', (mid, name, dose, cat, now_str))
        else:
            # Vergleich auf Änderungen (name, dose, cat)
            if (current[1] != name or current[2] != dose or current[3] != cat):
                # Alte Version schließen
                out_conn.execute("UPDATE dim_medication SET SCD_valid_to = ? WHERE med_key = ?", (now_str, current[0]))
                # Neue Version anlegen
                out_conn.execute('''
                    INSERT INTO dim_medication (med_id, name, dosage_mg, category, SCD_valid_from)
                    VALUES (?, ?, ?, ?, ?)
                ''', (mid, name, dose, cat, now_str))
    
    # --- dim_lifestyle (SCD Type 2) ---
    ls_input = in_conn.execute("SELECT user_id, is_smoker, movement_type FROM master_lifestyle").fetchall()
    for uid, smoker, move in ls_input:
        current = out_conn.execute('''
            SELECT lifestyle_key, is_smoker, movement_type FROM dim_lifestyle 
            WHERE user_id = ? AND SCD_valid_to = '9999-12-31'
        ''', (uid,)).fetchone()
        
        if not current:
            out_conn.execute('''
                INSERT INTO dim_lifestyle (user_id, is_smoker, movement_type, SCD_valid_from)
                VALUES (?, ?, ?, ?)
            ''', (uid, smoker, move, now_str))
        else:
            if (current[1] != int(smoker) or current[2] != move):
                out_conn.execute("UPDATE dim_lifestyle SET SCD_valid_to = ? WHERE lifestyle_key = ?", (now_str, current[0]))
                out_conn.execute('''
                    INSERT INTO dim_lifestyle (user_id, is_smoker, movement_type, SCD_valid_from)
                    VALUES (?, ?, ?, ?)
                ''', (uid, smoker, move, now_str))
    
    # --- dim_date (Stammdaten-Generierung) ---
    res = in_conn.execute("SELECT MIN(SUBSTR(timestamp, 1, 10)), MAX(SUBSTR(timestamp, 1, 10)) FROM raw_blood_pressure").fetchone()
    min_date, max_date = res[0], res[1]
    
    if min_date and max_date:
        start = datetime.strptime(min_date, '%Y-%m-%d')
        end = datetime.strptime(max_date, '%Y-%m-%d')
        curr = start
        while curr <= end:
            dk = int(curr.strftime('%Y%m%d'))
            out_conn.execute('''
                INSERT OR IGNORE INTO dim_date (date_key, full_date, day, month, year, day_name, is_weekend)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (dk, curr.strftime('%Y-%m-%d'), curr.day, curr.month, curr.year, curr.strftime('%A'), curr.weekday() >= 5))
            curr += timedelta(days=1)
            
    out_conn.commit()
    in_conn.close()
    out_conn.close()

def migrate_facts():
    print("Befülle Faktentabelle (Inkremental mit Dublettenprüfung)...")
    in_conn = sqlite3.connect(INPUT_DB)
    out_conn = sqlite3.connect(DWH_DB)
    
    time_map = {'morgens': 8, 'mittags': 13, 'abends': 19, 'nachts': 23}
    
    bp_data = in_conn.execute('''
        SELECT user_id, timestamp, systolic, diastolic, pulse 
        FROM raw_blood_pressure
    ''').fetchall()
    
    for user_id, ts, sys, dia, pul in bp_data:
        dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
        date_key = int(dt.strftime('%Y%m%d'))
        time_key = dt.strftime('%H:%M')
        
        # 1. Aktuellen Lifestyle Surrogate Key holen
        l_key_res = out_conn.execute("SELECT lifestyle_key FROM dim_lifestyle WHERE user_id = ? AND SCD_valid_to = '9999-12-31'", (user_id,)).fetchone()
        l_key = l_key_res[0] if l_key_res else None
        
        # 2. Aktuellen Medikation Surrogate Key holen (passend zur geplanten Einnahme)
        med_plan = in_conn.execute("SELECT time_of_day, medication_id FROM user_medication_plan WHERE user_id = ? AND is_active = 1", (user_id,)).fetchall()
        
        is_post = False
        m_key = 1 # Default
        
        for tod, mid in med_plan:
            planned_hour = time_map.get(tod.lower())
            if planned_hour is not None and planned_hour <= dt.hour < (planned_hour + 4):
                is_post = True
                # Den aktuell gültigen Surrogate Key für diese MedID holen
                m_key_res = out_conn.execute("SELECT med_key FROM dim_medication WHERE med_id = ? AND SCD_valid_to = '9999-12-31'", (mid,)).fetchone()
                if m_key_res: m_key = m_key_res[0]
        
        # 3. Aktivitätsdaten holen
        activity = in_conn.execute("SELECT steps, weight_kg, activity_minutes FROM raw_activity_daily WHERE user_id = ? AND date = ?", (user_id, dt.strftime('%Y-%m-%d'))).fetchone()
        steps = activity[0] if activity else None
        weight = activity[1] if activity else None
        act_min = activity[2] if activity else None
        
        # 4. Inkrementelles Insert (IGNORIEREN falls Dublette)
        out_conn.execute('''
            INSERT OR IGNORE INTO fact_health_metrics (
                user_id, date_key, time_key, med_key, lifestyle_key,
                systolic, diastolic, pulse, steps_hourly, weight_kg, activity_minutes,
                is_post_medication, pulse_pressure
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, date_key, time_key, m_key, l_key, sys, dia, pul, steps, weight, act_min, is_post, sys - dia))
        
    out_conn.commit()
    in_conn.close()
    out_conn.close()

def main():
    print("=== START DWH TRANSFORMATION ===")
    init_dwh()
    migrate_dimensions()
    migrate_facts()
    print("=== DWH TRANSFORMATION BEENDET ===")

if __name__ == "__main__":
    main()
