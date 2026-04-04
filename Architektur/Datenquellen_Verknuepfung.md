# Datenquellen-Verknüpfung und Struktur

Dieses Dokument beschreibt die Organisation der Rohdaten im Verzeichnis `data/01_raw` und die Logik, mit der die verschiedenen Datenquellen (Blutdruck-App und Smartwatch) miteinander verknüpft werden.

## 1. Verzeichnisstruktur (Multi-User-Konzept)

Um das System für mehrere Patienten skalierbar zu machen, werden die Rohdaten in nutzerspezifischen Unterverzeichnissen abgelegt. Jedes Verzeichnis entspricht einem Patienten (z. B. `patient_001`).

### Aufbau pro Patient:
`data/01_raw/patient_<ID>/`
- `csv/`: Enthält den Datenexport der Blutdruck-App (`HealthForYouApp_DataExport.csv`). In dieser Datei sind die SVD-Werte (Systolisch, Diastolisch, Puls) gespeichert.
- `json/`: Enthält den Google Takeout Export (JSON-Dateien) der Smartwatch. Hier liegen die Aktivitätsdaten (Schritte, Kalorien, Schlaf).
- `docs/`: Enthält begleitende Dokumente wie PDF-Exporte der App.

---

## 2. Verknüpfungslogik

Die Daten aus den unterschiedlichen Quellen werden über zwei Ebenen miteinander verknüpft:

### Ebene 1: Patienten-Zuordnung (Ordner-Ebene)
Alle Dateien innerhalb des Ordners `patient_001` werden beim Import der internen `user_id = 1` in der Datenbank zugeordnet. Das ETL-Skript liest den Ordnernamen aus und weist die Daten entsprechend zu.

### Ebene 2: Zeitliche Korrelation (Datensatz-Ebene)
Da Blutdruckmessungen und Smartwatch-Daten (z. B. Schritte) zu unterschiedlichen Zeiten generiert werden, erfolgt die Verknüpfung über den **Zeitstempel**.

- **Blutdruck (CSV)**: Besitzt Spalten für `Datum` und `Uhrzeit`.
- **Aktivität (JSON)**: Besitzt detaillierte Zeitstempel (`startTimeNanos` / `endTimeNanos`).

**Beispiel für eine Verknüpfung (Join):**
Ein Blutdruckwert von 12:05 Uhr wird mit der Anzahl der Schritte korreliert, die in dem Zeitfenster (z. B. 11:00 - 12:00 Uhr) direkt *vor* der Messung aufgezeichnet wurden.

---

## 3. Datenformate und SVD-Mapping

| Quelldaten-Feld | Datenbank-Feld (Input) | Beschreibung |
| :--- | :--- | :--- |
| `Sys` (CSV) | `systolic` | S-Wert (Systolischer Druck) |
| `Dia` (CSV) | `diastolic` | D-Wert (Diastolischer Druck) |
| `Puls` (CSV) | `pulse` | V-Wert (Variabilität/Puls) |
| `Schrittzahl` (CSV/JSON) | `steps` | Tägliche Bewegung |
| `Gewicht` (CSV/JSON) | `weight_kg` | Aus der Smartwatch-Synchronisation |

---

## 4. Erweiterbarkeit
Um einen neuen Nutzer hinzuzufügen, muss lediglich ein neuer Ordner (z. B. `patient_002`) angelegt und die entsprechenden Dateien dort abgelegt werden. Das System erkennt den neuen Nutzer beim nächsten Import-Lauf automatisch.
