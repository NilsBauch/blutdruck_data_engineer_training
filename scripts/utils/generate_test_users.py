# ==============================================================================
# SCRIPT: generate_test_users.py
# BESCHREIBUNG: Generiert realistische, anonymisierte Patienten-Testdaten.
#               Simulation von Blutdruck (mit Peak-Effekt), Medikation & Sport.
# AUFRUF: py scripts/utils/generate_test_users.py
# ERGEBNIS: Ordnerstruktur unter 'data/01_raw/' pro Patient mit CSVs und JSONs.
# ==============================================================================

import csv
import json
import random
import shutil
from datetime import datetime, timedelta
import os

# --- KONFIGURATION & PFADE ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', '01_raw')

# Patienten-Liste
patients = [
    {"id": 2, "med": "Ramipril", "dose": 5.0, "age": 62, "gender": "m"},
    {"id": 3, "med": "Candesartan", "dose": 8.0, "age": 71, "gender": "w"},
    {"id": 4, "med": "Amlodipin", "dose": 5.0, "age": 55, "gender": "m"},
    {"id": 5, "med": "Bisoprolol", "dose": 2.5, "age": 68, "gender": "w"},
    {"id": 6, "med": "Ramipril", "dose": 2.5, "age": 45, "gender": "m", "sport": True} # User mit Sporteffekt
]

def clear_old_data(patient_dir):
    """Bereinigt alte CSV/JSON-Dateien im Patienten-Ordner."""
    csv_dir = os.path.join(patient_dir, 'csv')
    fit_dir = os.path.join(patient_dir, 'json', 'Takeout', 'Google Fit', 'Tägliche Aktivitätswerte')
    
    if os.path.exists(csv_dir):
        shutil.rmtree(csv_dir)
    os.makedirs(csv_dir, exist_ok=True)
    
    if os.path.exists(fit_dir):
        shutil.rmtree(fit_dir)
    os.makedirs(fit_dir, exist_ok=True)

def generate_blood_pressure_data(p_id, p_info, target_file, days=30, med_start_day=14, has_sport=False):
    """Generiert 30 Tage Blutdruckdaten mit klarem Medikationseffekt (4h Peak)."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    with open(target_file, mode='w', encoding='utf-8', newline='') as f:
        # Header
        f.write("Benutzerangaben\n\n")
        f.write(f"Vorname;Patient\n")
        f.write(f"Nachname;{p_id:03d}\n")
        f.write(f"Geburtstag;01.01.{2026 - p_info['age']}\n")
        f.write(f"Geschlecht;{'Männlich' if p_info['gender'] == 'm' else 'Weiblich'}\n")
        f.write(f"Größe;{random.randint(160, 190)} cm\n\n")
        f.write("Zeitraum\n\n")
        f.write(f"von;{start_date.strftime('%d.%m.%Y')}\n")
        f.write(f"bis;{end_date.strftime('%d.%m.%Y')}\n\n")
        f.write("Ausgewählte Kategorien\n\n")
        f.write(f"Blutdruck;{days * 3}\n\n")
        f.write("BLUTDRUCK\n")
        f.write("Datum;Uhrzeit;Sys;Dia;Puls;MAD;Manuell hinzugefügt\n")
        writer = csv.writer(f, delimiter=';')
        
        for day in range(days - 1, -1, -1):
            current_date = start_date + timedelta(days=day)
            date_str = current_date.strftime("%d.%m.%Y")
            
            is_active_day = has_sport and day >= med_start_day
            
            for hour in [20, 11, 8]:
                time_str = f"{hour:02d}:{random.randint(0, 59):02d}"
                
                # Baseline Werte (Hypertension Baseline)
                sys_base = random.randint(148, 160)
                dia_base = random.randint(95, 102)
                pulse_base = random.randint(78, 85)
                
                if day >= med_start_day:
                    # Medikationseffekt (Einnahme um 08:00)
                    if hour == 8:
                        # Baseline am Morgen (Noch keine volle Wirkung)
                        red_sys = random.randint(0, 3) 
                        red_dia = random.randint(0, 2)
                    elif hour == 11:
                        # PEAK Effekt (nach 3-4h)
                        red_sys = random.randint(22, 32)
                        red_dia = random.randint(12, 18)
                    else:
                        # Abend (Moderater Effekt)
                        red_sys = random.randint(10, 15)
                        red_dia = random.randint(5, 8)
                    
                    sys = sys_base - red_sys
                    dia = dia_base - red_dia
                    
                    # Sporteffekt (Puls-Korrelation)
                    if is_active_day:
                        pulse = 60 + random.randint(-2, 3) # Konstanter niedriger Puls
                        sys -= random.randint(5, 8)       # Leichte zusätzliche BP-Senkung
                    else:
                        pulse = pulse_base - random.randint(0, 5) # Nur med. Senkung
                else:
                    sys = sys_base
                    dia = dia_base
                    pulse = pulse_base
                
                mad = int(dia + (sys - dia) / 3)
                writer.writerow([date_str, time_str, sys, dia, pulse, mad, 0])
        
        f.write("\nMAD = Mittlerer arterieller Druck\n")

def generate_activity_data(patient_dir, days=30, sport_start_day=14, has_sport=False):
    """Generiert tägliche Aktivitäts-CSVs im exakten Google Fit Format (langer Header)."""
    fit_dir = os.path.join(patient_dir, 'json', 'Takeout', 'Google Fit', 'Tägliche Aktivitätswerte')
    os.makedirs(fit_dir, exist_ok=True)
    
    # Original Header
    header = [
        "Beginn", "Ende", "Anzahl der Aktivitätsminuten", "Kalorien (kcal)", "Distanz (m)", 
        "Kardiopunkte", "Kardiominuten", "Durchschnittliche Herzfrequenz (bpm)", 
        "Maximale Herzfrequenz (bpm)", "Minimale Herzfrequenz (bpm)", "Minimaler Breitengrad (Grad)", 
        "Minimaler Längengrad (Grad)", "Maximaler Breitengrad (Grad)", "Maximaler Längengrad (Grad)", 
        "Durchschnittliche Sauerstoffsättigung (%)", "Max. Sauerstoffsättigung (%)", 
        "Min. Sauerstoffsättigung (%)", "Durchschnittliche Durchflussmenge der Sauerstoffgabe (L/Min.)", 
        "Max. Durchflussmenge der Sauerstoffgabe (L/Min.)", "Min. Durchflussmenge der Sauerstoffgabe (L/Min.)", 
        "Verabreichungsform für Sauerstofftherapie", "Sauerstoffsättigungssystem", 
        "Verfahren zur Messung der Sauerstoffsättigung", "Durchschnittsgeschwindigkeit (m/s)", 
        "Maximale Geschwindigkeit (m/s)", "Minimale Geschwindigkeit (m/s)", "Schrittzahl", 
        "Durchschnittsgewicht (kg)", "Maximales Gewicht (kg)", "Minimales Gewicht (kg)"
    ]
    
    start_date = datetime.now() - timedelta(days=days)
    
    for day in range(days):
        current_date = start_date + timedelta(days=day)
        filename = current_date.strftime("%Y-%m-%d.csv")
        filepath = os.path.join(fit_dir, filename)
        
        if has_sport and day >= sport_start_day:
            steps = random.randint(8000, 15000)
            active_mins = random.randint(45, 90)
        else:
            steps = random.randint(1500, 4500)
            active_mins = random.randint(5, 20)
            
        weight = 85.0 - (0.1 * day if has_sport and day >= sport_start_day else 0)
        
        # Wir erstellen eine Zeile (vereinfacht im Vergleich zum Original, aber mit korrektem Header)
        # Das Ladeskript sucht nur nach den Indexen im Header.
        with open(filepath, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            
            # Dummy-Zeile mit den relevanten Werten
            row = [""] * len(header)
            row[header.index("Beginn")] = "08:00:00.000+01:00"
            row[header.index("Ende")] = "20:00:00.000+01:00"
            row[header.index("Anzahl der Aktivitätsminuten")] = active_mins
            row[header.index("Schrittzahl")] = steps
            row[header.index("Durchschnittsgewicht (kg)")] = f"{weight:.2f}".replace('.', ',')
            writer.writerow(row)

def main():
    print(f"Starte Generierung von {len(patients)} (exakte Formate)...")
    
    for p in patients:
        p_id_str = f"patient_{p['id']:03d}"
        p_dir = os.path.join(RAW_DATA_DIR, p_id_str)
        
        os.makedirs(os.path.join(p_dir, 'csv'), exist_ok=True)
        os.makedirs(os.path.join(p_dir, 'profile'), exist_ok=True)
        
        # 1. Profil
        profile = {
            "user_info": {"name": f"Patient {p['id']:03d}", "age": p['age'], "gender": p['gender']},
            "lifestyle": {"is_smoker": False, "movement_type": "sportlich" if p.get('sport') else "wenig"},
            "medication_plan": [{"medication_name": p['med'], "dosage_mg": p['dose'], "time_of_day": "morgens"}]
        }
        with open(os.path.join(p_dir, 'profile', 'user_profile.json'), 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2)
            
        # 2. Blutdruck (Exakt)
        generate_blood_pressure_data(
            p['id'], p,
            os.path.join(p_dir, 'csv', 'HealthForYouApp_DataExport.csv'),
            has_sport=p.get('sport', False)
        )
        
        # 3. Aktivität (Exakt)
        generate_activity_data(p_dir, has_sport=p.get('sport', False))
        
        print(f" -> {p_id_str} (exakt) generiert.")

    print("\nAlle Daten erfolgreich unter data/01_raw/ generiert.")

if __name__ == "__main__":
    main()
