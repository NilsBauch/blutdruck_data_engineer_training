import csv
import json
import random
from datetime import datetime, timedelta
import os

# Pfad anpassen zum raw data ordner
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "01_raw")
os.makedirs(BASE_DIR, exist_ok=True)

patients = [101, 102, 103, 104, 105]

def generate_data():
    start_date = datetime(2023, 10, 1)
    
    # 1. Blutdruck Daten (CSV)
    bp_file = os.path.join(BASE_DIR, "blood_pressure.csv")
    with open(bp_file, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["patient_id", "timestamp", "systolic", "diastolic", "heart_rate"])
        
        for p in patients:
            for day in range(30):
                current_date = start_date + timedelta(days=day)
                # Morgenmessung
                m_time = current_date + timedelta(hours=random.randint(7, 9), minutes=random.randint(0, 59))
                sys = random.randint(120, 165)
                dia = random.randint(80, 105)
                hr = random.randint(60, 95)
                writer.writerow([p, m_time.isoformat(), sys, dia, hr])
                
                # Abendmessung
                e_time = current_date + timedelta(hours=random.randint(18, 20), minutes=random.randint(0, 59))
                sys = max(110, sys - random.randint(5, 20)) # Abends oft leicht niedriger
                dia = max(70, dia - random.randint(5, 15))
                hr = random.randint(65, 85)
                writer.writerow([p, e_time.isoformat(), sys, dia, hr])

    # 2. Bewegungsdaten (JSON)
    activity_data = []
    for p in patients:
        for day in range(30):
            current_date = start_date + timedelta(days=day)
            steps = random.randint(1500, 12000)
            inactivity = random.randint(30, 240) # Minuten max Inaktivität
            activity_data.append({
                "patient_id": p,
                "date": current_date.strftime("%Y-%m-%d"),
                "daily_steps": steps,
                "inactivity_periods_longer_1h": random.randint(0, 4),
                "max_inactivity_duration_minutes": inactivity
            })
            
    activity_file = os.path.join(BASE_DIR, "activity.json")
    with open(activity_file, "w", encoding='utf-8') as f:
        json.dump(activity_data, f, indent=4)

    # 3. Medikationsdaten (CSV)
    med_file = os.path.join(BASE_DIR, "medication.csv")
    meds = ["Ramipril", "Bisoprolol", "Amlodipin", "Candesartan"]
    with open(med_file, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["patient_id", "date", "medication_name", "dosage_mg", "taken_time"])
        
        for p in patients:
            patient_med = random.choice(meds)
            patient_dose = random.choice([5, 10, 20])
            for day in range(30):
                # 10% Chance, dass Medikament vergessen wurde 
                if random.random() > 0.1:
                    current_date = start_date + timedelta(days=day)
                    taken_time = current_date + timedelta(hours=random.randint(7, 10), minutes=random.randint(0, 59))
                    writer.writerow([p, current_date.strftime("%Y-%m-%d"), patient_med, patient_dose, taken_time.isoformat()])

    print(f"Erfolgreich Mock-Daten unter generiert: {BASE_DIR}")

if __name__ == '__main__':
    generate_data()
