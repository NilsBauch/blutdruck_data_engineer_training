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
    
    for p_id in patients:
        # Ordnerstruktur für den Patienten erstellen
        patient_folder = f"patient_{p_id:03d}"
        p_base_dir = os.path.join(BASE_DIR, patient_folder)
        
        csv_dir = os.path.join(p_base_dir, "csv")
        json_dir = os.path.join(p_base_dir, "json", "Takeout", "Google Fit", "Tägliche Aktivitätswerte")
        profile_dir = os.path.join(p_base_dir, "profile")
        
        os.makedirs(csv_dir, exist_ok=True)
        os.makedirs(json_dir, exist_ok=True)
        os.makedirs(profile_dir, exist_ok=True)
        
        # 1. Blutdruck Daten (CSV) - Erwartet von load_raw_data.py
        # Wir nennen die Datei so, wie es das Ladeskript erwartet (beliebiger .csv Name im csv-Ordner)
        bp_file = os.path.join(csv_dir, "blood_pressure_export.csv")
        with open(bp_file, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';') # Ladeskript erwartet Semikolon
            writer.writerow(["Datum", "Uhrzeit", "Systolisch", "Diastolisch", "Puls", "Gewicht", "Manuell"])
            
            for day in range(30):
                current_date = start_date + timedelta(days=day)
                date_str = current_date.strftime("%d.%m.%Y")
                
                # Morgenmessung
                m_time = current_date + timedelta(hours=random.randint(7, 9), minutes=random.randint(0, 59))
                sys = random.randint(120, 165)
                dia = random.randint(80, 105)
                hr = random.randint(60, 95)
                writer.writerow([date_str, m_time.strftime("%H:%M"), sys, dia, hr, 0, 0])
                
                # Abendmessung
                e_time = current_date + timedelta(hours=random.randint(18, 20), minutes=random.randint(0, 59))
                sys = max(110, sys - random.randint(5, 20))
                dia = max(70, dia - random.randint(5, 15))
                hr = random.randint(65, 85)
                writer.writerow([date_str, e_time.strftime("%H:%M"), sys, dia, hr, 0, 0])

        # 2. Bewegungsdaten (JSON -> konvertiert zu CSV-Dateien pro Tag für Google Fit Simulation)
        # load_raw_data.py erwartet Dateien im Format YYYY-MM-DD.csv im Google Fit Ordner
        for day in range(30):
            current_date = start_date + timedelta(days=day)
            day_str = current_date.strftime("%Y-%m-%d")
            activity_file = os.path.join(json_dir, f"{day_str}.csv")
            
            steps = random.randint(1500, 12000)
            weight = random.uniform(70.0, 95.0)
            active_mins = random.randint(10, 90)
            
            with open(activity_file, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Zeit", "Schrittzahl", "Durchschnittsgewicht (kg)", "Anzahl der Aktivitätsminuten"])
                writer.writerow([day_str, steps, f"{weight:.2f}".replace('.', ','), active_mins])

        # 3. Nutzerprofil & Medikationsplan (JSON)
        profile_file = os.path.join(profile_dir, "user_profile.json")
        meds = [
            {"name": "Ramipril", "dose": 5.0},
            {"name": "Bisoprolol", "dose": 2.5},
            {"name": "Amlodipin", "dose": 5.0},
            {"name": "Candesartan", "dose": 8.0}
        ]
        chosen_med = random.choice(meds)
        
        profile_data = {
            "user_info": {
                "name": f"Patient {p_id:03d}",
                "age": random.randint(60, 85),
                "gender": random.choice(["m", "w"])
            },
            "lifestyle": {
                "is_smoker": random.choice([True, False]),
                "movement_type": random.choice(["wenig", "mittel", "sportlich"])
            },
            "medication_plan": [
                {
                    "medication_name": chosen_med["name"],
                    "dosage_mg": chosen_med["dose"],
                    "time_of_day": "morgens"
                }
            ]
        }
        with open(profile_file, "w", encoding='utf-8') as f:
            json.dump(profile_data, f, indent=2)

    print(f"Erfolgreich Mock-Daten für {len(patients)} Patienten generiert unter: {BASE_DIR}")

if __name__ == '__main__':
    generate_data()
