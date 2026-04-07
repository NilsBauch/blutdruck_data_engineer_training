import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DWH_DB = os.path.join(BASE_DIR, 'database', 'blutdruck_dwh.db')

def verify():
    if not os.path.exists(DWH_DB):
        print(f"Fehler: {DWH_DB} nicht gefunden.")
        return

    conn = sqlite3.connect(DWH_DB)
    cursor = conn.cursor()
    
    query = """
    SELECT 
        f.time_key, 
        f.systolic, 
        f.diastolic, 
        d.day_name, 
        f.is_post_medication, 
        f.pulse_pressure,
        f.steps_hourly
    FROM fact_health_metrics f
    JOIN dim_date d ON f.date_key = d.date_key
    LIMIT 5;
    """
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        print(f"{'Zeit':<10} | {'Sys':<5} | {'Dia':<5} | {'Tag':<10} | {'Meds?':<5} | {'PP':<5} | {'Steps':<5}")
        print("-" * 65)
        for row in rows:
            print(f"{row[0]:<10} | {row[1]:<5} | {row[2]:<5} | {row[3]:<10} | {row[4]:<5} | {row[5]:<5} | {row[6]:<5}")
        
        # Count check
        cursor.execute("SELECT COUNT(*) FROM fact_health_metrics")
        count = cursor.fetchone()[0]
        print(f"\nGesamtanzahl Datensätze im DWH: {count}")
        
    except Exception as e:
        print(f"Fehler bei der Abfrage: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    verify()
