# Aktivitätsdiagramm (Whitebox): UC5 - Analysen interaktiv filtern & explorieren

Hier wird die reaktive Schleife gezeigt, die abläuft, wenn der Benutzer im laufenden Dashboard mit Filtern oder Grafiken interagiert.

![Diagramm](images/activity_diagram_uc5_0.png)

```mermaid
flowchart TD
    %% Swimlanes
    subgraph Browser ["Browser / Streamlit-Frontend"]
        U1(("User-Event")) --> A1["Filter anpassen (z.B. Datum, Wert oder Metrik ändern)"]
        A2["Streamlit sendet State-Change an Server"]
        A3["Neue Grafiken/Tabellen werden im Browser eingeblendet"]
    end

    subgraph Server ["Streamlit Backend (Python)"]
        S1["Registriert Änderung in Sidebar/Widgets"]
        S2["Gesamtes Python-Skript wird automatisch neu ausgeführt"]
        S3["Neue SQL-Query mit aktualisierten WHERE-Bedingungen bauen"]
        S4["Grafik-Bibliothek (z.B. Plotly/Altair) rendert neue Charts"]
    end

    subgraph DWH ["SQLite DWH"]
        D1["Empfängt gefilterte Anfrage"]
        D2["Führt Abfrage auf transformierten Fakten aus"]
        D3["Sendet aggregiertes Resultset zurück"]
    end

    %% Flusslogik
    A1 --> A2
    A2 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> D1
    
    D1 --> D2
    D2 --> D3
    D3 --> S4
    
    S4 --> A3
    
    %% Wartezustand erreichen
    A3 --> U2(("Wartet auf neues Event"))
```

