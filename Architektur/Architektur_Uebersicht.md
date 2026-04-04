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
3.  **Master Data / Stammdaten (Medikation & Lifestyle):**
    *   **Methode:** Direkte Pflege und Bereitstellung über eine SQLite-Datenbank.
    *   **Format:** `SQLite3`. Enthält den Medikamenten-Katalog und benutzerspezifische Profile (Raucher status, Sport-Intensität).

---

## 2. Architekturdiagramm (Mermaid)

```mermaid
flowchart TD
    %% Quellen
    subgraph Quellen ["Datenquellen"]
        A["Mobile App: HealthForYou"]
        B["Smartwatch (via Google Fit)"]
        M[("Stammdaten: Medikation & Lifestyle \n (Format: SQLite3)")]
    end

    %% Export/Rohdaten Layer (Umstrukturiert)
    subgraph Export ["Staging & Rohdaten (patient_001)"]
        C[("csv/ \n (Blutdruck-Export)")]
        D[("json/ \n (Smartwatch-Export)")]
    end

    %% Pipeline Layer
    subgraph ETL ["ETL-Datenpipeline (Python 3)"]
        E("1. Data Ingestion/Extraction")
        F("2. Transformation & Bereinigung")
        G("3. Feature Engineering & Harmonisierung")
    end

    %% Storage Layer
    subgraph Storage ["Data Warehouse"]
        H[("SQLite3 Datenbank \n Star Schema: Fakten & Dimensionen")]
    end

    %% Presentation Layer
    subgraph Analyse ["Business Intelligence"]
        I(["Interaktives Streamlit Dashboard"])
    end

    %% Datenfluss
    A -->|"CSV-Export generieren"| C
    B -->|"Google Takeout anfordern"| D
    M -->|"Tabellen einlesen"| E

    C -->|"Liest CSV in Pandas/Polars"| E
    D -->|"Liest JSON/CSV in Pandas/Polars"| E

    E -->|"Rohdaten-DataFrames"| F
    F -->|"Typisierte, bereinigte Daten"| G
    G -->|"Aggregierte Intervalle & Metriken"| H

    H <-->|"SQL Query (z. B. via SQLAlchemy)"| I

    %% Styling
    classDef source fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef raw fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef process fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef dwh fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px;
    classDef dash fill:#ffebee,stroke:#c62828,stroke-width:2px;

    class A,B,M source;
    class C,D raw;
    class E,F,G process;
    class H dwh;
    class I dash;
```
