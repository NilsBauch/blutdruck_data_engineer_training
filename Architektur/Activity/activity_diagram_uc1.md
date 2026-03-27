# Aktivitätsdiagramm (Whitebox): UC1 - Datenexporte im Raw-Ordner ablegen

Dieses Diagramm modelliert den ersten Use-Case und zeigt im Whitebox-Stil, wie der Benutzer oder das Sensorensystem (z.B. Health App) die Daten in das Dateisystem des Data-Engineering-Projekts einspielt.

```mermaid
flowchart TD
    %% Swimlanes definieren
    subgraph Akteur [Externe Quelle / Patient]
        direction TB
        Start((Start)) --> A1[Datenexport in App anfordern / Sensor auslesen]
        A1 --> A2[Daten im CSV/JSON-Format generieren]
        A2 --> A3[Datei manuell ins Projekt-Verzeichnis kopieren]
    end

    subgraph System [Lokales Dateisystem]
        direction TB
        S1[Speichervorgang in /data/raw/ ausführen]
        S2[Prüfen, ob Datei-Endung korrekt ist]
        S3{Dateityp gültig?}
        S4[Datei im Raw-Ordner abgelegt]
        S5[Fehlermeldung (OS Level)]
    end

    %% Verknüpfungen zwischen den Swimlanes
    A3 --> S1
    S1 --> S2
    S2 --> S3
    S3 -- Ja --> S4
    S3 -- Nein --> S5
    
    S4 --> Ziel((Ende))
    S5 --> Ziel
```
