import sqlite3
import os
from datetime import datetime, timedelta

# Pfade
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DB = os.path.join(BASE_DIR, 'database', 'blutdruck_input.db')
DWH_DB = os.path.join(BASE_DIR, 'database', 'blutdruck_dwh.db')
SCHEMA_SQL = os.path.join(BASE_DIR, 'database', 'dwh_schema.sql')

def init_dwh():
    print("Initialisiere DWH Schema...")
    if os.path.exists(DWH_DB):
        os.remove(DWH_DB)
    
    conn = sqlite3.connect(DWH_DB)
    with open(SCHEMA_SQL, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()

def migrate_dimensions():
    print("Migriere Dimensionen...")
    in_conn = sqlite3.connect(INPUT_DB)
    out_conn = sqlite3.connect(DWH_DB)
    
    # dim_user (Anonymisiert: Gender statt Name)
    users = in_conn.execute("SELECT user_id, gender, age FROM master_lifestyle").fetchall()
    out_conn.executemany("INSERT INTO dim_user (user_id, gender, age) VALUES (?, ?, ?)", users)
    
    # dim_medication
    meds = in_conn.execute("SELECT med_id, name, dose_mg, description FROM master_medications").fetchall()
    out_conn.executemany("INSERT INTO dim_medication (med_id, name, dosage_mg, category) VALUES (?, ?, ?, ?)", meds)
    
    # dim_lifestyle
    ls = in_conn.execute("SELECT user_id, is_smoker, movement_type FROM master_lifestyle").fetchall()
    out_conn.executemany("INSERT INTO dim_lifestyle (lifestyle_id, is_smoker, movement_type) VALUES (?, ?, ?)", ls)
    
    # dim_date (für alle relevanten Tage generieren)
    # Zeitraum ermitteln
    min_date = in_conn.execute("SELECT MIN(SUBSTR(timestamp, 1, 10)) FROM raw_blood_pressure").fetchone()[0]
    max_date = in_conn.execute("SELECT MAX(SUBSTR(timestamp, 1, 10)) FROM raw_blood_pressure").fetchone()[0]
    
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
    print("Befülle Faktentabelle (Mess-Ebene)...")
    in_conn = sqlite3.connect(INPUT_DB)
    out_conn = sqlite3.connect(DWH_DB)
    
    # Basis-Werte für Zeiten definieren (morgens=8h, etc.)
    time_map = {'morgens': 8, 'mittags': 13, 'abends': 19, 'nachts': 23}
    
    # Wir nehmen Blutdruck-Messungen als Basis für die Fakten
    bp_data = in_conn.execute('''
        SELECT user_id, timestamp, systolic, diastolic, pulse 
        FROM raw_blood_pressure
    ''').fetchall()
    
    for user_id, ts, sys, dia, pul in bp_data:
        dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
        date_key = int(dt.strftime('%Y%m%d'))
        time_key = dt.strftime('%H:%M')
        
        # Aktivitätsdaten für diesen Tag holen
        activity = in_conn.execute('''
            SELECT steps, weight_kg, activity_minutes 
            FROM raw_activity_daily 
            WHERE user_id = ? AND date = ?
        ''', (user_id, dt.strftime('%Y-%m-%d'))).fetchone()
        
        steps = activity[0] if activity else None
        weight = activity[1] if activity else None
        act_min = activity[2] if activity else None
        
        # Prüfung auf Medikations-Status (is_post_medication)
        med_plan = in_conn.execute('''
            SELECT time_of_day, medication_id 
            FROM user_medication_plan 
            WHERE user_id = ? AND is_active = 1
        ''', (user_id,)).fetchall()
        
        is_post = False
        active_med_id = 1 # Fallback, falls kein Plan existiert
        
        for tod, med_id in med_plan:
            planned_hour = time_map.get(tod.lower())
            if planned_hour is not None:
                # Logik: Messung liegt innerhalb von 4h NACH geplanter Einnahme
                if planned_hour <= dt.hour < (planned_hour + 4):
                    is_post = True
                    active_med_id = med_id
        
        out_conn.execute('''
            INSERT INTO fact_health_metrics (
                user_id, date_key, time_key, med_id, lifestyle_id,
                systolic, diastolic, pulse, steps_hourly, weight_kg, activity_minutes,
                is_post_medication, pulse_pressure
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, date_key, time_key, active_med_id, user_id, sys, dia, pul, steps, weight, act_min, is_post, sys - dia))
        
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
