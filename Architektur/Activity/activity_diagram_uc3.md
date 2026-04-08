# Aktivitätsdiagramm (Whitebox): UC3 - Daten transformieren & in DWH integrieren

Dieses Diagramm zeigt im Detail, was innerhalb des in UC2 ausgelösten Sub-Prozesses beim Transformieren und Laden passiert, insbesondere die Interaktion zwischen Pandas und der SQLite-Datenbank.

![Diagramm](images/activity_diagram_uc3_0.png)

```mermaid
flowchart TD
    %% Startpunkt des Includes
    Start(("Beginn UC3")) --> P1

    subgraph Python ["Python (SCD & Fact Transformation)"]
        P1["Rohdaten aus Staging laden"]
        P2["Dimensions-Check: Existiert Business Key im DWH?"]
        P3{"Änderung erkannt?"}
        P4["SCD 2: Alte Version schließen (SCD_valid_to = now)"]
        P5["SCD 2: Neue Version öffnen (SCD_valid_to = 9999)"]
        P6["Inkrementelle Fakten-Vorbereitung (Lookup Keys)"]
    end

    subgraph SQLite ["SQLite Data Warehouse"]
        S1["Verbindung zur DWH-DB aufbauen"]
        S2["SCD-Updates & Inserts ausführen"]
        S3["Fakten mit UNIQUE-Constraint laden (INSERT OR IGNORE)"]
        S4["Transaktion abschließen (COMMIT)"]
        S5["Verbindung schließen"]
    end

    %% Verknüpfungen
    P1 --> P2
    P2 --> P3
    P3 -- Ja --> P4
    P4 --> P5
    P5 --> P6
    P3 -- Nein --> P6
    
    P6 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S5 --> End(("Ende / Rückgabe an UC2"))
```

