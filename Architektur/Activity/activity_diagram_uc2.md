# Aktivitätsdiagramm (Whitebox): UC2 - ETL-Workflow ausführen

Dieses Diagramm zeigt den Start und die Ablauflogik des ETL-Hauptskripts. Da Use-Case 3 zwingend inkludiert ist, wird er hier als Sub-Prozess (Referenz) dargestellt.

![Aktivitätsdiagramm UC2](../images/activity_diagram_uc2.png)

![Diagramm](../images/activity_diagram_uc2_0.png)

```mermaid
flowchart TD
    %% Swimlanes definieren
    subgraph User ["Data Engineer / Scheduler"]
        Start(("Start")) --> A1["Orchestrierung triggern (python scripts/run_pipeline.py)"]
    end

    subgraph Python ["Python Runtime (Orchestrator)"]
        P1["1. Initialisierung (DB-Schemata IF NOT EXISTS)"]
        P2["2. Ingestion (load_raw_data.py)"]
        P3["3. Transformation (build_dwh.py)"]
        P4[["Sub-Prozess: UC3 Transformation & DWH-Load"]]
        P5["Logging: Status & Metriken prüfen"]
    end

    %% Verknüpfungen
    A1 --> P1
    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> P5
    P5 --> End(("Ende"))
    
    P7 --> End(("Ende"))
    P8 --> End
```

