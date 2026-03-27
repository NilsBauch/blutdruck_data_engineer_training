# Aktivitätsdiagramm (Whitebox): UC2 - ETL-Workflow ausführen

Dieses Diagramm zeigt den Start und die Ablauflogik des ETL-Hauptskripts. Da Use-Case 3 zwingend inkludiert ist, wird er hier als Sub-Prozess (Referenz) dargestellt.

```mermaid
flowchart TD
    %% Swimlanes definieren
    subgraph User [Data Engineer / Scheduler]
        Start((Start)) --> A1[ETL-Skript manuell oder per Job triggern\nz.B. python main_etl.py]
    end

    subgraph Python [Python Laufzeitumgebung (ETL-Master)]
        P1[Skript initialisiert Logging und Parameter]
        P2[Nach neuen Dateien im Raw-Ordner scannen]
        P3{Dateien gefunden?}
        P4[Daten aus CSV/JSON in Pandas einlesen]
        P5[[Sub-Prozess: UC3 Transformation & DWH-Load]]
        P6[Rohdaten in /data/archive/ verschieben / taggen]
        P7[Logging: ETL-Lauf erfolgreich abgeschlossen]
        P8[Logging: Keine neuen Daten, Abbruch]
    end

    %% Verknüpfungen
    A1 --> P1
    P1 --> P2
    P2 --> P3
    P3 -- Ja (Rohdaten vorhanden) --> P4
    P4 --> P5
    P5 --> P6
    P6 --> P7
    P3 -- Nein --> P8
    
    P7 --> End((Ende))
    P8 --> End
```
