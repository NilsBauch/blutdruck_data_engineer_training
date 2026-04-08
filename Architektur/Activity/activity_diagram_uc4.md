# Aktivitätsdiagramm (Whitebox): UC4 - Dashboard starten

Dieses Diagramm verdeutlicht die Architektur beim Starten der analytischen Oberfläche. Es repräsentiert die Initialisierung der Streamlit-Webanwendung und die erste Datenbereitstellung.

![Diagramm](images/activity_diagram_uc4_0.png)

```mermaid
flowchart TD
    %% Swimlanes
    subgraph UI ["Benutzer / Webbrowser"]
        U1(("Start")) --> A1["Webbrowser öffnen / Localhost aufrufen"]
        U1 --> A0["Kommandozeile: streamlit run dashboard.py (Server-Prozess starten)"]
        A0 --> S1
        A1 --> U2["Initiale Benutzeroberfläche laden"]
        U2 --> U3["Erste Dashboard-Ansicht (Overview) betrachten"]
    end

    subgraph Server ["Streamlit Backend"]
        S1["Streamlit-Dienst fährt hoch (Port 8501)"]
        S2["App-Code wird von oben nach unten ausgeführt"]
        S3["Initiale Datenbankverbindung herstellen"]
        S4["Basisdaten via SELECT-Query laden"]
        S5["Standard-Filterwerte setzen (z.B. letzte 30 Tage)"]
        S6["UI-Komponenten (Layout, Sidebar) generieren"]
    end

    subgraph DWH ["SQLite DWH"]
        D1["Verbindungsanforderung akzeptieren"]
        D2["SQL-Anfrage nach Gesamtdaten verarbeiten"]
        D3["Tabelle an Python zurückliefern"]
    end

    %% Verknüpfungen
    S1 --> S2
    S2 --> S3
    
    S3 --> D1
    D1 --> D2
    D2 --> D3
    D3 --> S4
    
    S4 --> S5
    S5 --> S6
    
    %% Datenfluss an Oberfläche
    S6 --> U2
    
    %% Ende des Bootstraps
    U3 --> End(("Wartet auf Interaktion / UC5"))
```

