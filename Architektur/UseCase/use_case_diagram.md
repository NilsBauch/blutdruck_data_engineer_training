# Use-Case-Diagramm: Health Monitoring (Blutdruck & Aktivität)

Dieses Modell beschreibt die funktionalen Hauptanwendungsfälle deines Data-Engineering-Projekts aus der Perspektive der interagierenden Akteure.

## 1. Übersicht der Akteure
* **Patient / Data Engineer:** Die handelnde Person, die Daten zur Verfügung stellt, den Pipeline-Prozess überwacht und das analytische Dashboard konsumiert.
* **Sensoren / Tracking-Apps (Externes System):** Geräte wie das Blutdruckmessgerät und die Smartwatch, die Rohdaten erzeugen.

---

## 2. UML Use-Case Diagramm (Mermaid)

```mermaid
flowchart LR
    %% Style für die Akteure definieren
    classDef actor fill:#f4f4f4,stroke:#333,stroke-width:2px,shape:circle;

    %% Definition der Akteure
    User((Patient / Anwender))
    Sensors((Tracking-Apps / Sensoren))

    %% Zuweisung des Styles
    class User,Sensors actor

    %% Definition der Systemgrenzen
    subgraph System["Health Monitoring System (ETL + DWH + Dashboard)"]
        direction TB
        
        UC1(["Datenexporte im Raw-Ordner ablegen"])
        UC2(["ETL-Workflow ausführen"])
        UC3(["Daten transformieren & in DWH integrieren"])
        UC4(["Dashboard (Streamlit) starten"])
        UC5(["Analysen interaktiv filtern & explorieren"])
    end

    %% Verknüpfungen (Communication Links)
    User --> UC1
    User --> UC2
    User --> UC4
    User --> UC5
    
    Sensors --> UC1
    
    %% Abhängigkeiten (Includes / Extends)
    UC2 -.->|<<includes>>| UC3
```

---

## 3. Beschreibung der Anwendungsfälle (Use-Cases)

| Use-Case | Kurzbeschreibung |
| :--- | :--- |
| **Datenexporte ablegen** | Die Rohdaten (CSV/JSON) werden durch den Akteur oder das Sensorsystem periodisch in der definierten Ablagestruktur generiert und bereitgestellt. |
| **ETL-Workflow ausführen** | Der Anwender startet (manuell oder zeitgesteuert) das Master-Skript der Datenpipeline. |
| **Daten transformieren & integrieren** | Innerhalb des Workflows reinigt das System automatisch die Zeitleisten, reichert die Features an und schreibt die aggregierten Fakten ins DWH (Star-Schema). *Die Ausführung des ETL-Workflows inkludiert diesen Schritt zwingend (`<<includes>>`).* |
| **Dashboard starten** | Der Anwender ruft die Streamlit-Webanwendung auf, die sich direkt mit dem lokalen Data Warehouse verbindet. |
| **Analysen filtern & explorieren** | Der Anwender justiert Betrachtungszeiträume, filtert nach Metriken (z. B. "nur hohe Inaktivität") und analysiert die grafischen Korrelationen zwischen Medikamenten, Blutdruck und Bewegung. |
