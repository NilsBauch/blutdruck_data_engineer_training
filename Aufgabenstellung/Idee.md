# Projektidee: Health Monitoring für ältere Menschen
Fokus: Blutdruck, Bewegung & Medikation

## Kernidee
Ein End-to-End-System zur Datenanalyse für Hypertonie-Patienten, das folgende Datenpunkte zusammenführt:

- Blutdruckverläufe
- Bewegungsprofil und körperliche Aktivität (Schritte, Inaktivitätsphasen)
- Medikationsplan (Bedarfs- und Dauermedikation wie Blutdrucksenker)

Ziel der Arbeit ist es, zu analysieren, wie sich der Blutdruck in Abhängigkeit von Bewegung, Tageszeit und Medikamentengabe entwickelt. Darüber hinaus soll untersucht werden, ob sich Risikomuster – wie beispielsweise dauerhaft hoher Blutdruck bei langanhaltender Inaktivität – automatisiert erkennen lassen.

---

## Formale Anforderungen der Projektarbeit
Das Konzept adressiert direkt die vorgegebenen Projektanforderungen:

> "Die Daten sollen aus mindestens drei unterschiedlichen Quellen stammen (z. B. CSV, JSON, Excel/XLSX, Datenbanken, REST APIs oder Open Data Portale)."

> "Die Ergebnisse der OLAP-Analysen werden anschließend in einem Streamlit-Dashboard visualisiert."

---

## Datenquellen und Schnittstellen

### 1. Kardiovaskuläre Daten (Blutdruck)
- Bereitgestellt als CSV- oder Excel-Export aus Blutdruckmessgeräten oder Gesundheits-Apps.
- Für die Entwicklung: Einsatz von generierten, synthetischen Datenstrukturen, die realistische Messwerte simulieren.

### 2. Bewegungs- und Aktivitätsdaten
- Nutzung von Wearable- oder Smartphone-Metriken (Aktivitätsminuten, Schrittzahl) im JSON-/CSV-Format.
- Alternativ: Anbindung eines öffentlichen Open-Data-Sets.

### 3. Medikationshistorie
- Excel- oder CSV-Tabellen zur Dokumentation der Verabreichung.
- Notwendige Attribute:
  - Patient-ID
  - Medikamentenpräparat
  - Dosierung (mg)
  - Einnahmezeitpunkt

### 4. Optionale Erweiterung: Wetterdaten
- Externe REST-API zur Abfrage von Außentemperatur und Luftdruck zum Messzeitpunkt.
- Hypothese: Es bestehen messbare Korrelationen zwischen saisonalen oder wetterbedingten Einflüssen und dem Blutdruck.

---

## Geplante OLAP-Analysen und Fragestellungen

### Einfluss der Bewegung auf den Blutdruck
- Signifikanzanalyse des durchschnittlichen Blutdrucks an Tagen mit hoher vs. niedriger Aktivität.
- Identifikation spezifischer Tageszeiten mit unzureichend sinkendem Blutdruck trotz körperlicher Betätigung.

### Einfluss der Medikation auf den Blutdruck
- Zeitverlaufsanalyse des Blutdrucks in den ersten Stunden nach Verabreichung eines Wirkstoffs.
- Vergleich der durchschnittlichen Senkungseffekte unterschiedlicher Medikamentenklassen.

### Kombinierte Faktoren (Bewegung und Medikation)
- Untersucht, ob sportliche Aktivität im Anschluss an eine Medikamenteneinnahme synergetische Effekte auf die Blutdrucksenkung hat.
- Identifikation einer Risikogruppe: Patienten, bei denen trotz Medikation kombiniert mit Bewegung der Blutdruck anhaltend zu hoch ist.

### Präventives Monitoring (Sturz- und Gefahrenanalyse)
- Auswertung außergewöhnlich langer Inaktivitätsphasen als Indikator für mögliche Stürze oder gesundheitliche Vorfälle.
- Alarmierungslogik bei Kombination aus hoher Inaktivität, verpasster Medikation und messbar erhöhtem Blutdruck.

---

## Grobe technische Architektur (ETL & DWH)

### 1. Extract
- Flat-File-Lader (CSV/Excel) für strukturierte Gesundheits- und Medikationsdaten.
- JSON-Verarbeitung für hierarchische Wearable-Daten.

### 2. Transform
- Harmonisierung der Zeitzonen und -achsen (Aggregation auf standardisierte Intervalle, z.B. 15 Minuten).
- Relationales Mapping der Daten über die `Patient-ID` und den Erfassungszeitraum.
- Feature Engineering zur Ableitung neuer Kennzahlen ("Gesamtschritte im 2-h-Intervall", "Vergangene Zeit seit letzter Dosis").

### 3. Load
- **Data Warehouse Ansatz (Star-Schema)**:
  - Faktentabelle für alle gemessenen Vitalwerte und Aktivitäten.
  - Dimensionen für Patienten, Zeit, Medikamente und Aktivitäten.
- **Data Marts**: Abgeleitete Tabellen für spezifische Dashboard-Ansichten ("Blutdruck x Bewegung").

### 4. Visualisierung
- Entwicklung einer analytischen Streamlit-Applikation.
- Interaktive Zeitreihenanalyse, Pivotierungsmöglichkeiten und aggregierte KPIs zur schnellen Triage.

---

## Datenschutz und Ethik
Da Gesundheitsdaten besonders sensibel sind (gemäß DSGVO Art. 9), gelten für dieses Projekt strikte Vorgaben:
- Es werden ausschließlich rein synthetische Daten genutzt.
- Die Arbeit versteht sich als technische Machbarkeitsstudie für eine Datenpipeline, nicht als Basis für medizinische Diagnosen der realen Welt.
