# Architektur-Übersicht: Health Monitoring Projekt

Das folgende Diagramm zeigt die Gesamtarchitektur des Data Engineering Projekts. 
Es veranschaulicht den Weg von den Datenquellen über die Extraktion und ETL-Verarbeitung bis hin zur Speicherung und Visualisierung. 

Das Setup basiert auf **Python 3** als primärer Programmiersprache für den gesamten ETL-Prozess und **SQLite3** für die persistente Datenhaltung im Data Warehouse.

## Datenquellen und Formate

1.  **HealthForYou App (Blutdruck & Medikation):** 
    *   **Methode:** Manueller Datenexport direkt aus der Applikation.
    *   **Format:** `CSV` (Comma-Separated Values). Enthält typischerweise Tabellenstrukturen mit definierten Spalten wie Datum, Uhrzeit, Systole, Diastole, Puls.
2.  **Google Fit / Smartwatch (Aktivitäts- & Bewegungsdaten):**
    *   **Methode:** Automatisierter/Manueller Export aller Gesundheits- und Fitnessdaten über den **Google Takeout** Dienst.
    *   **Formate:** 
        *   `JSON` (JavaScript Object Notation): Sehr tiefgreifende und komplexe Fitnessdaten (z. B. feingranulare Schritt-Aggregate, Schlafanalyse, tägliche Aktivitäts-Metriken) werden von Google Fit zumeist als unstrukturierte oder halbstrukturierte JSON-Dateien ausgegeben, oft iteriert in diversen Unterordnern.
        *   `CSV`: Standard-Aktivitäten-Metriken über den gesamten Export-Zeitraum liegen teilweise strukturiert vor.
        *   `TCX` (Training Center XML): Besonders detaillierte Einzel-Aufzeichnungen (wie bspw. ein konkreter Spaziergang oder Lauf mit GPS-Tracking) werden als XML-Struktur (TCX) mitgeliefert.

**Für dieses Projekt fokussieren wir uns bei Google Fit primär auf die Aufbereitung der `JSON`- sowie etwaiger `CSV`-Rohdaten.**

---

## Architekturdiagramm (Mermaid)

```mermaid
flowchart TD
    %% Quellen
    subgraph Quellen ["Datenquellen"]
        A["Mobile App: HealthForYou"]
        B["Smartwatch (via Google Fit)"]
    end

    %% Export/Rohdaten Layer
    subgraph Export ["Staging & Rohdaten-Ablage"]
        C[("Manueller App-Export \n (Format: CSV)")]
        D[("Google Takeout Export \n (Formate: JSON, CSV, TCX)")]
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

    class A,B source;
    class C,D raw;
    class E,F,G process;
    class H dwh;
    class I dash;
```
