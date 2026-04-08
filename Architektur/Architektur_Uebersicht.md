# Architektur-Übersicht: Health Monitoring Projekt

Das folgende Diagramm zeigt die Gesamtarchitektur des Data Engineering Projekts. 
Es veranschaulicht den Weg von den Datenquellen über die Extraktion und ETL-Verarbeitung bis hin zur Speicherung und Visualisierung. 

Das Setup basiert auf **Python 3** als primärer Programmiersprache für den gesamten ETL-Prozess und **SQLite3** für die persistente Datenhaltung im Data Warehouse.

### Aufbau der Rohdaten (`01_raw`)
Um mehrere Patienten zu unterstützen, werden die Daten in nutzerspezifischen Unterordnern gespeichert. Eine detaillierte Erläuterung der Verknüpfungslogik finden Sie in der [Datenquellen-Verknüpfung](file:///c:/Users/nilsb/OneDrive/Nils/weiterbildung/DataEngineer/Projektarbeit/Blutdruck/Architektur/Datenquellen_Verknuepfung.md).

## 1. Datenquellen und Formate

1.  **HealthForYou App (Blutdruck & Medikation):** 
    *   **Methode:** Manueller Datenexport direkt aus der Applikation.
    *   **Dateipfad:** `data/01_raw/patient_<ID>/csv/HealthForYouApp_DataExport.csv`
    *   **Format:** `CSV` (SVD-Werte: Systole, Diastole, Puls).
2.  **Google Fit / Smartwatch (Aktivitäts- & Bewegungsdaten):**
    *   **Methode:** Export aller Fitnessdaten über **Google Takeout**.
    *   **Dateipfad:** `data/01_raw/patient_<ID>/json/`
    *   **Formate:** `JSON` (detaillierte Schritte, Schlaf), `CSV` (Tageszusammenfassungen).
3.  **Stammdaten (Medikation & Lifestyle):**
    *   **Medikation:** Der Medikamenten-Katalog wird über SQL-Dateien (`database/populate_master_data.sql`) gepflegt.
    *   **Lifestyle:** Individuelle Patientenprofile (Raucherstatus, Bewegungstyp) werden über die Datei `user_profile.json` im Profil-Ordner des Patienten definiert.

---

## 2. Architekturdiagramm

![Architektur Übersicht](./images/architektur_uebersicht.png)

![Diagramm](./images/architektur_uebersicht_0.png)

```mermaid
flowchart TD
    %% Quellen
    subgraph Quellen ["Datenquellen"]
        A["Mobile App: HealthForYou"]
        B["Smartwatch (via Google Fit)"]
        M_MED[("Katalog: Medikation \n (Format: SQL/SQLite)")]
        M_LIFE[("Profil: Lifestyle \n (Format: JSON)")]
    end

    %% Export/Rohdaten Layer (Umstrukturiert)
    subgraph Export ["Staging & Rohdaten (Patienten-Ordner)"]
        C[("csv/ \n (Blutdruck-Export)")]
        D[("json/ \n (Smartwatch-Export)")]
    end

    %% Pipeline Layer
    subgraph ETL ["ETL-Orchestrierung (run_pipeline.py)"]
        E("1. Data Ingestion (load_raw_data.py)")
        F("2. Inkrementelle Transformation")
        G("3. SCD Type 2 & Historisierung")
    end

    %% Storage Layer
    subgraph Storage ["Data Warehouse"]
        H[("SQLite3 Datenbank \n Star Schema (SCD 2)")]
    end

    %% Presentation Layer
    subgraph Analyse ["Business Intelligence"]
        I(["Interaktives Streamlit Dashboard"])
    end

    %% Datenfluss
    A -->|"CSV-Export"| C
    B -->|"Google Takeout"| D
    M_MED & M_LIFE -->|"Tabellen / Parsing"| E

    C -->|"Import"| E
    D -->|"Import"| E

    E -->|"Staging Data"| F
    F -->|"Deltas"| G
    G -->|"Fakten & Dimensionen"| H

    H <-->|"SQL Queries"| I

    %% Styling
    classDef source fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef raw fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef process fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef dwh fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px;
    classDef dash fill:#ffebee,stroke:#c62828,stroke-width:2px;

    class A,B,M_MED,M_LIFE source;
    class C,D raw;
    class E,F,G process;
    class H dwh;
    class I dash;
```
