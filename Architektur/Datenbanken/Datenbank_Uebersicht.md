# Datenbank- & ETL-Übersicht

Diese Dokumentation beschreibt die Schichtenarchitektur der Blutdruck-Monitoring-Plattform, die verwendeten SQLite-Datenbanken und die ETL-Logik.

## 1. Datenfluss-Diagramm

![Datenfluss Übersicht](../images/datenbank_uebersicht.png)

```mermaid
flowchart TD
    %% Datenquellen
    subgraph Quellen ["1. Rohdaten (Filesystem)"]
        direction LR
        CSV_BP["Blutdruck-App \n (HealthForYouApp_DataExport.csv)"]
        JSON_STEPS["Smartwatch-Schritte \n (Google Fit .json)"]
        CSV_ACT["Smartwatch-Aktivität \n (Tägliche_Aktivität.csv)"]
    end

    %% ETL Prozess
    subgraph ETL ["2. ETL-Orchestrierung (Python)"]
        P0["run_pipeline.py \n (Master Script)"]
        P1["load_raw_data.py \n (Extract & Load)"]
        P2["build_dwh.py \n (Transform)"]
    end

    %% Staging Area
    subgraph Staging ["3. Staging Area (blutdruck_input.db)"]
        direction TB
        T1[("master_lifestyle \n (Profil, Alter, Pfade)")]
        T2[("master_medications \n (Katalog)")]
        T3[("raw_blood_pressure \n (Rohwerte)")]
        T4[("raw_activity_daily \n (Schritte)")]
    end

    %% Warehouse
    subgraph DWH ["4. Analytics Layer (blutdruck_dwh.db)"]
        F1[("Fact: fact_health_metrics \n (mit Surrogate Keys)")]
        D1[("Dim: dim_lifestyle \n (SCD Type 2)")]
        D2[("Dim: dim_medication \n (SCD Type 2)")]
    end

    %% Verbindungen
    CSV_BP & JSON_STEPS & CSV_ACT --> P1
    P0 --> P1 & P2
    P1 --> T1 & T2 & T3 & T4
    T1 & T2 & T3 & T4 --> P2
    P2 --> F1
    F1 --- D1 & D2

    %% Styling
    classDef file fill:#fffde7,stroke:#fbc02d,stroke-width:2px;
    classDef db fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef script fill:#f1f8e9,stroke:#558b2f,stroke-width:2px;

    class CSV_BP,JSON_STEPS,CSV_ACT file;
    class T1,T2,T3,T4,F1,D1,D2 db;
    class P1,P2 script;
```

---

## 2. Schichtenarchitektur

Die Daten fließen in drei Hauptschichten durch das System:

1.  **Raw Layer (Dateisystem)**: In Ordnern organisierte CSV- und JSON-Exporte (patient_001, etc.).
2.  **Staging Area (Ingestion / SQLite)**: `blutdruck_input.db`. Rohdaten-Import und Bereitstellung der Stammdaten.
3.  **Data Warehouse (Analytics / SQLite)**: `blutdruck_dwh.db` (Geplant). Optimiertes Star-Schema für Abfragen und Dashboards.

---

## 2. Staging Area (`blutdruck_input.db`)

Diese Datenbank dient der technischen Übernahme der Rohdaten. Hier findet noch keine Änderung der Granularität statt.

### Stammdaten (Master Data)
*   **`master_medications`**: Katalog aller verfügbaren Medikamente (Name, Dosis in mg).
*   **`master_lifestyle`**: Benutzerprofile (Alter, Raucher-Status, Bewegungstyp) sowie das dynamische Folder-Mapping (`raw_data_folder`).
*   **`user_medication_plan`**: Verknüpfung von Patient, Medikament und Einnahmezeitpunkt (morgens, abends, etc.).

### Rohdaten-Tabellen (Raw Area)
*   **`raw_blood_pressure`**: Importierte SVD-Werte (Systolisch, Diastolisch, Puls) mit Zeitstempel.
*   **`raw_activity_daily`**: Tägliche Zusammenfassung von Schritten, Gewicht und Aktivitätsminuten.

---

## 3. ETL-Skripte & Logik

Die Transformation wird durch Python-Skripte gesteuert:

*   **`init_db.py`**: Initialisiert das Schema und befüllt die Stammdaten aus den SQL-Dateien.
*   **`load_raw_data.py`**: 
    - **Metadata-driven**: Liest aus `master_lifestyle`, welche Patienten-Ordner existieren.
    - **Parsing**: Verarbeitet HealthForYou-CSVs (Blutdruck) und Google Fit-CSVs (Smartwatch).
    - **Transformation**: Normiert Zeitstempel auf ISO-Format (`YYYY-MM-DD HH:MM:SS`).

---

## 4. Zielzustand: Warehouse (DWH)

Das geplante Warehouse folgt dem **Star-Schema**, um komplexe Analysen zu beschleunigen (z.B. "Wie verhält sich der Blutdruck 2 Stunden nach der Tabletteneinnahme bei Bewegung?").

### Geplante Tabellen:
*   **`fact_health_metrics`**: Die zentrale Tabelle, die Blutdruck, Aktivität und Medikation auf Stunden- oder Tagesebene verknüpft.
*   **`dim_patient`**: Patienten-Dimension (Alter, Bewegungstyp).
*   **`dim_medication`**: Medikations-Dimension.
*   **`dim_time`**: Zeit-Dimension (Attribute wie Wochentag, Tageszeit-Cluster).

---

## 5. Speicherorte

*   Rohdaten: `data/01_raw/`
*   SQL-Skripte: `database/`
*   Datenbank-Dateien: `database/*.db`
*   Python-ETL: `scripts/`

