import zlib
import base64
import urllib.request
import os

IMAGE_DIR = r'c:\Users\nilsb\OneDrive\Nils\weiterbildung\DataEngineer\Projektarbeit\Blutdruck\Architektur\images'

def generate_kroki_image(mermaid_code, output_path):
    print(f"Erstelle {output_path}...")
    try:
        payload = base64.urlsafe_b64encode(zlib.compress(mermaid_code.encode('utf-8'), 9)).decode('ascii')
        url = f"https://kroki.io/mermaid/png/{payload}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"Fehler: {e}")
    return False

# ERM (Business-DB)
erm_code = """
erDiagram
    PATIENT ||--o{ MEDICATION_PLAN : has
    PATIENT ||--o{ BLOOD_PRESSURE : records
    PATIENT ||--o{ ACTIVITY_DAILY : tracks
    MEDICATION ||--o{ MEDICATION_PLAN : includes

    PATIENT {
        int user_id PK
        string name
        int age
        string lifestyle_info
    }
    MEDICATION {
        int med_id PK
        string name
        float dose_mg
    }
    MEDICATION_PLAN {
        int id PK
        int user_id FK
        int med_id FK
        string time_of_day
    }
    BLOOD_PRESSURE {
        int id PK
        int user_id FK
        datetime ts
        int systolic
        int diastolic
    }
    ACTIVITY_DAILY {
        int id PK
        int user_id FK
        date day
        int steps
    }
"""

# mER (DWH)
mer_code = """
erDiagram
    FACT_HEALTH_METRICS }o--|| DIM_USER : who
    FACT_HEALTH_METRICS }o--|| DIM_DATE : when
    FACT_HEALTH_METRICS }o--|| DIM_MEDICATION : treatment
    FACT_HEALTH_METRICS }o--|| DIM_LIFESTYLE : context

    FACT_HEALTH_METRICS {
        int fact_id PK
        int user_id FK
        int date_key FK
        int med_id FK
        int lifestyle_id FK
        int systolic
        int diastolic
        int pulse_pressure
        int steps
    }
    DIM_USER {
        int user_id PK
        string name
        int age
    }
    DIM_DATE {
        int date_key PK
        date full_date
        string day_name
        boolean is_weekend
    }
    DIM_MEDICATION {
        int med_id PK
        string name
        float dosage_mg
    }
    DIM_LIFESTYLE {
        int lifestyle_id PK
        boolean is_smoker
        string movement_type
        string SCD_valid_from
        string SCD_valid_to
    }
"""

if __name__ == "__main__":
    generate_kroki_image(erm_code, os.path.join(IMAGE_DIR, 'design_erm_business.png'))
    generate_kroki_image(mer_code, os.path.join(IMAGE_DIR, 'design_mer_dwh.png'))
