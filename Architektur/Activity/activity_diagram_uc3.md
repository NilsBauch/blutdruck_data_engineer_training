# Aktivitätsdiagramm (Whitebox): UC3 - Daten transformieren & in DWH integrieren

Dieses Diagramm zeigt im Detail, was innerhalb des in UC2 ausgelösten Sub-Prozesses beim Transformieren und Laden passiert, insbesondere die Interaktion zwischen Pandas und der SQLite-Datenbank.

```mermaid
flowchart TD
    %% Startpunkt des Includes
    Start(("Beginn UC3")) --> P1

    subgraph Python ["Python (Pandas Transformation)"]
        P1["Rohdaten (DataFrames) annehmen"]
        P2["Datums- und Zeitstempel normalisieren"]
        P3["Fehlende Werte (Null/NaN) interpolieren oder droppen"]
        P4["Fakten aggregieren (z.B. Durchschnitt pro Tag)"]
        P5["Dimensionstabellen (Zeit, Patient) aktualisieren"]
    end

    subgraph SQLite ["SQLite Data Warehouse"]
        S1["Verbindung zur DB aufbauen (SQLAlchemy)"]
        S2["Transaktion starten (BEGIN)"]
        S3["Dimensionstabellen einfügen (INSERT OR IGNORE)"]
        S4["Faktentabelle schreiben (INSERT)"]
        S5{"Fehler beim Laden?"}
        S6["Transaktion bestätigen (COMMIT)"]
        S7["Transaktion verwerfen (ROLLBACK)"]
        S8["Verbindung schließen"]
    end

    %% Verknüpfungen
    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> P5
    
    P5 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    
    S5 -- Nein --> S6
    S6 --> S8
    
    S5 -- Ja (z.B. Constraint Violation) --> S7
    S7 --> S8
    
    S8 --> End(("Ende / Rückgabe an UC2"))
```
