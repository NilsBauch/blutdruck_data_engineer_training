# Doxygen-Dokumentationssystem

Diese Datei beschreibt, wie die technische Dokumentation in diesem Projekt mit **Doxygen** funktioniert, 
welche Dateien entscheidend sind und wie der Workflow für Entwickler aussieht.

## 1. Übersicht & Ziel
Doxygen wird verwendet, um aus dem Quellcode (Python, SQL) und Markdown-Dateien automatisch eine strukturierte 
technische Dokumentation zu generieren. Ziel ist es, eine stets aktuelle Übersicht über die Pipeline-Logik, 
Funktionen und Datenbank-Schemata zu haben, ohne die Dokumentation separat pflegen zu müssen.

## 2. Zentrale Komponenten

### Konfiguration
*   **[Doxyfile](file:///c:/Users/nilsb/OneDrive/Nils/weiterbildung/DataEngineer/Projektarbeit/Blutdruck/Doxyfile)**: 
Die zentrale Konfigurationsdatei. Sie legt fest, welche Verzeichnisse gescannt werden, welche Dateitypen (`.py`, `.sql`, `.md`) 
berücksichtigt werden und wohin die Ergebnisse geschrieben werden.

### Automatisierung
*   **[update_docs.bat](file:///c:/Users/nilsb/OneDrive/Nils/weiterbildung/DataEngineer/Projektarbeit/Blutdruck/update_docs.bat)**: 
Ein Windows-Batch-Skript, das den gesamten Aktualisierungsprozess startet. Es führt zuerst die Bild-Migration/Diagramm-Erstellung 
aus und startet danach den Doxygen-Prozess.
*   **[scripts/utils/refresh_docs.py](file:///c:/Users/nilsb/OneDrive/Nils/weiterbildung/DataEngineer/Projektarbeit/Blutdruck/scripts/utils/refresh_docs.py)**: 
Orchestriert Vorbereitungsschritte wie das Umwandeln von Mermaid-Diagrammen in statische Bilder, damit diese in der 
Doxygen-HTML-Ausgabe korrekt angezeigt werden.

### Inhalte
*   **[docs/Mainpage.md](file:///c:/Users/nilsb/OneDrive/Nils/weiterbildung/DataEngineer/Projektarbeit/Blutdruck/docs/Mainpage.md)**: 
Definiert die Startseite der HTML-Dokumentation. Hier finden sich meist architektonische Übersichten und Use-Cases.

---

## 3. Workflow für Entwickler

Wenn du Codeänderungen vornimmst oder neue Skripte hinzufügst, folge diesem Workflow:

1.  **Code dokumentieren**: Verwende Doxygen-Tags direkt im Code (siehe unten).
2.  **Dokumentation generieren**: Führe die Datei `update_docs.bat` im Hauptverzeichnis aus.
3.  **Prüfen**: Öffne `docs/doxygen_output/html/index.html` in deinem Browser, um das Ergebnis zu kontrollieren.

---

## 4. Dokumentations-Standard im Code

### Python-Beispiel
In Python-Skripten werden spezielle Kommentare mit doppeltem Raute-Zeichen (`##`) oder `@`-Tags verwendet:

```python
## @file script_name.py
#  @brief Kurze Beschreibung des Moduls.

## @brief Berechnet einen Wert.
#  @param input_val Der Eingabewert.
#  @return Das Ergebnis der Berechnung.
def calculate(input_val):
    return input_val * 2
```

### SQL-Beispiel
Auch SQL-Dateien können dokumentiert werden, indem Doxygen-Tags in den Kommentaren platziert werden:

```sql
--! @file schema.sql
--! @brief Definition der Haupttabellen.

CREATE TABLE users ( ... );
```

---

## 5. Output-Verzeichnis
Das Ergebnis der Dokumentation findet sich immer unter:
`docs/doxygen_output/html/`

> [!TIP]
> Die Datei `index.html` ist der Einstiegspunkt für die Website.
