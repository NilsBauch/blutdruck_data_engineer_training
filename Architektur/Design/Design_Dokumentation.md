# Design-Dokumentation: Health Monitoring Plattform

Dieses Dokument beschreibt den Aufbau und die Datenstrategie für das Blutdruck-Monitoring. Es wird sauber zwischen dem **Dateneingang (Business-DB)** und dem **Auswertungs-Bereich (Data Warehouse)** getrennt.

---

## 1. Zielsetzung des Projekts

Das Ziel ist die Untersuchung von Blutdruck, Puls und Bewegung in Verbindung mit Medikamenten. 

### Die Fragen an die Daten:
*   Hat die Tablette (z.B. Ramipril) den Blutdruck in den ersten 4 Stunden wirklich gesenkt?
*   Helfen mehr Schritte am Tag dabei, den Ruhepuls zu senken?
*   Gibt es Unterschiede zwischen Werktagen (Stress?) und dem Wochenende?
*   **Historie**: Wie haben sich die Werte verändert, nachdem jemand angefangen hat, mehr Sport zu treiben?

---

## 2. Der Dateneingang (Business-DB / Staging)

Die `blutdruck_input.db` dient als Zwischenlager (Staging). Hier fließen die Daten aus drei unterschiedlichen Quellen zusammen.

### Datenquellen (Übersicht)
1.  **Blutdruck (CSV):** Direkter Export aus der Smartphone-App.
2.  **Aktivität (CSV/JSON):** Rohdaten-Abzug der Smartwatch (Google Takeout).
3.  **Nutzerprofil & Plan (JSON):** Eine dedizierte Steuerdatei (`user_profile.json`), die das Profil und die Medikation verwaltet.

### Speicherplatz (Kalkulation)
In einer Hochrechnung für **100 Leute über 5 Jahre** ergeben sich folgende Werte:
*   **Blutdruck**: 2 Messungen pro Tag = 365.000 Zeilen (ca. 22 MB).
*   **Aktivität**: 1 Eintrag pro Tag = 182.500 Zeilen (ca. 7 MB).
*   **Insgesamt**: Das Datenvolumen liegt bei ca. **50 MB** inklusive Indizes. Für SQLite ist das eine geringe Last und extrem performant.

### Datenbank-Design (Normalform)
Die Daten werden sauber getrennt gehalten. Patienten-Profile liegen in einer Tabelle, der Medikationsplan in einer anderen. Das spart Platz und verhindert, dass bei jeder Messung der Name des Patienten mitgeführt werden muss (Daten-Redundanz vermeiden).

### Datenmodell (ERM)
![ERM Business DB](../images/design_erm_business.png)

---

## 3. Der Auswertungs-Bereich (Data Warehouse)

Die `blutdruck_dwh.db` ist für die Analyse optimiert. Hierfür wird ein **Star-Schema** eingesetzt.

### Wie das funktioniert:
In der Mitte liegt eine große **Fakten**: `fact_health_metrics` (Messwerte, Pulsdruck, Flags). Drumherum liegen **Dimensionen** (Nutzer, Zeit, Medikamente, Lifestyle), die einfach per Join verknüpft werden können. Das ist viel schneller als im verzweigten Eingangs-Modell zu suchen.

### Star-Schema Modell (mER)
![mER Star Schema](../images/design_mer_dwh.png)

---

## 4. Wie kommen die Daten rüber? (ETL & Mapping)

Ein Python-Skript (`build_dwh.py`) liest den Eingang aus, berechnet den **Pulsdruck** (Differenz zwischen den Werten) und ordnet die Schritte dem richtigen Tag zu.

### ETL Mapping Tabelle (Detailliert)

| Quelle (Eingangs-DB) | Tabellen-Spalte | Ziel (DWH-DB) | Ziel-Spalte | Transformation / Logik |
| :--- | :--- | :--- | :--- | :--- |
| `raw_blood_pressure`| `systolic` | `fact_health_metrics` | `systolic` | Direkte Übernahme |
| `raw_blood_pressure`| `diastolic` | `fact_health_metrics` | `diastolic` | Direkte Übernahme |
| `raw_blood_pressure`| `pulse` | `fact_health_metrics` | `pulse` | Direkte Übernahme |
| `raw_blood_pressure`| `sys - dia` | `fact_health_metrics` | `pulse_pressure` | Berechnung des Pulsdrucks |
| `raw_blood_pressure`| `timestamp` | `fact_health_metrics` | `date_key` | Konvertierung zu YYYYMMDD (FK) |
| `raw_blood_pressure`| `timestamp` | `fact_health_metrics` | `time_key` | Extraktion der Uhrzeit (HH:MM) |
| - | - | `fact_health_metrics` | **`med_key`** | Verknüpfung über aktuellen Surrogate Key |
| - | - | `fact_health_metrics` | **`lifestyle_key`** | Verknüpfung über aktuellen Surrogate Key |
| `raw_activity_daily`| `steps` | `fact_health_metrics` | `steps_hourly` | Zuordnung zum Tag der Messung |
| `raw_activity_daily`| `weight_kg` | `fact_health_metrics` | `weight_kg` | Direkte Übernahme |
| `raw_activity_daily`| `activity_minutes`| `fact_health_metrics` | `activity_minutes` | Direkte Übernahme |
| `master_lifestyle` | `movement_type` | `dim_lifestyle` | `movement_type` | Übernahme Aktivitätsstatus |
| `master_lifestyle` | `is_smoker` | `dim_lifestyle` | `is_smoker` | Übernahme Raucherstatus |
| `master_lifestyle` | `user_id` | `dim_user` | `user_id` | Migration Business Key |
| `master_lifestyle` | `age` | `dim_user` | `age` | Direkte Übernahme |
| `master_lifestyle` | `gender` | `dim_user` | `gender` | Übernahme (m/w/d) |
| `user_medication_plan`| `time_of_day` | `fact_health_metrics` | `is_post_medication` | `True`, falls Messung innerhalb 4h nach Einnahme |
| `master_medications`| `med_id` | `dim_medication` | `med_id` | Migration Business Key |
| `master_medications`| `name`, `dose_mg` | `dim_medication` | `name`, `dosage_mg` | Stammdaten-Migration |
| - | - | `fact_health_metrics` | `load_timestamp` | Technischer Zeitstamp beim Import |

---

## 5. Historie bewahren (SCD 2)

Das ist ein wichtiger Punkt im Data Engineering: Was passiert, wenn ein Patient sportlicher wird?

*   Wenn der Wert einfach überschrieben wird (SCD 1), sieht es im Zeitverlauf so aus, als ob der Status des Patienten *schon immer* aktuell war. Das verfälscht die historischen Blutdruckwerte.
*   Mit **SCD 2** wird eine neue Version des Datensatzes angelegt. Es ist somit genau ersichtlich: "Vom 01.01. bis 31.03. war der Status unsportlich, ab dem 01.04. sportlich".

### Technische Spalten:
Dazu werden zwei Zeitstempel genutzt:
*   `SCD_valid_from`: Ab wann gilt dieser Zustand?
*   `SCD_valid_to`: Bis wann galt dieser Zustand? (**9999-12-31** = aktuell gültig).

---

## Anhang: Technische Modelle (Mermaid)

*Hier liegen die Quellcodes für die Diagramme, falls du sie später für die Doku anpassen oder in ein anderes Format exportieren willst.*

### ERM (Business-DB)
![Diagramm](images/design_dokumentation_0.png)

```mermaid
flowchart TD
    %% Entitäten (Rechtecke)
    P[master_lifestyle]
    MP[user_medication_plan]
    BP[raw_blood_pressure]
    AD[raw_activity_daily]
    M[master_medications]

    %% Beziehungen (Rauten)
    REL_HAS{hat_plan}
    REL_REC{erfasst}
    REL_TRACK{trackt}
    REL_PLAN{gehört_zu}

    %% Attribute master_user_lifestyle
    P --- p1([<u>user_id</u>])
    P --- p3([age])
    P --- p4([gender])
    P --- p5([is_smoker])
    P --- p6([movement_type])
    P --- p7([raw_data_folder])

    %% Attribute master_medications
    M --- m1([<u>med_id</u>])
    M --- m2([name])
    M --- m3([dose_mg])
    M --- m4([description])

    %% Attribute user_medication_plan
    MP --- mp1([<u>plan_id</u>])
    MP --- mp2([user_id FK])
    MP --- mp3([medication_id FK])
    MP --- mp4([time_of_day])
    MP --- mp5([is_active])

    %% Attribute raw_blood_pressure
    BP --- bp1([<u>bp_id</u>])
    BP --- bp2([user_id FK])
    BP --- bp3([timestamp])
    BP --- bp4([systolic])
    BP --- bp5([diastolic])
    BP --- bp6([pulse])
    BP --- bp7([is_manual])

    %% Attribute raw_activity_daily
    AD --- ad1([<u>activity_id</u>])
    AD --- ad2([user_id FK])
    AD --- ad3([date])
    AD --- ad4([steps])
    AD --- ad5([activity_minutes])
    AD --- ad6([weight_kg])

    %% Verbindungen mit Kardinalitäten
    P -- 1 --- REL_HAS
    REL_HAS -- n --- MP
    P -- 1 --- REL_REC
    REL_REC -- n --- BP
    P -- 1 --- REL_TRACK
    REL_TRACK -- n --- AD
    M -- 1 --- REL_PLAN
    REL_PLAN -- n --- MP
```

### mER (Star-Schema)
![Diagramm](images/design_dokumentation_1.png)

```mermaid
erDiagram
    fact_health_metrics }o--|| dim_user : who
    fact_health_metrics }o--|| dim_date : when
    fact_health_metrics }o--|| dim_medication : treatment
    fact_health_metrics }o--|| dim_lifestyle : context

    fact_health_metrics {
        int fact_id PK
        int user_id FK
        int date_key FK
        string time_key
        int med_key FK
        int lifestyle_key FK
        int systolic
        int diastolic
        int pulse
        int steps_hourly
        float weight_kg
        int activity_minutes
        boolean is_post_medication
        int pulse_pressure
        datetime load_timestamp
    }
    dim_user {
        int user_id PK
        varchar(1) gender
        int age
    }
    dim_date {
        int date_key PK
        date full_date
        int day
        int month
        int year
        string day_name
        boolean is_weekend
    }
    dim_medication {
        int med_key PK
        int med_id
        string name
        float dosage_mg
        string category
        date SCD_valid_from
        date SCD_valid_to
    }
    dim_lifestyle {
        int lifestyle_key PK
        int user_id
        boolean is_smoker
        string movement_type
        date SCD_valid_from
        date SCD_valid_to
    }
```
