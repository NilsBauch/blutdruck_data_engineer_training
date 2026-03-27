# Anforderungsdefinition: Health Monitoring für ältere Menschen

Dieses Dokument fasst die wesentlichen Systemanforderungen für das Data Engineering Projekt zusammen. Die Einstufung hilft dabei, den Scope der Projektarbeit präzise abzugrenzen.

## 1. Funktionale Anforderungen (Functional Requirements)
*Diese Anforderungen definieren, **was** das fertige System fachlich und technisch leisten muss.*

* **[F-01] Datenextraktion:** Das System muss fähig sein, strukturierte Daten (CSV, Excel) für Blutdruck- und Medikationswerte sowie halbstrukturierte Formate (JSON) für Bewegungsdaten effizient einzulesen.
* **[F-02] Datentransformation & Bereinigung:** Vorhandene Inkonsistenzen (z. B. unterschiedliche Formate für Zeitstempel) müssen in der Staging-Area in ein einheitliches Format überführt werden.
* **[F-03] Harmonisierung der Zeitleisten:** Da Messwerte asynchron entstehen, müssen die Zeitstempel auf definierte Zeitfenster (z. B. aggregierte 15- oder 60-Minuten-Intervalle) gerundet werden.
* **[F-04] Datenintegration (Mapping):** Blutdruckmessungen, Bewegungsdaten und Medikationszeitpunkte müssen relational über Fremdschlüssel (`Patient-ID` und die korrespondierende `Zeit-ID`) logisch miteinander verknüpft werden.
* **[F-05] Feature Engineering:** Das System leitet komplexe Analyse-Merkmale eigenständig aus Rohdaten ab. Dazu gehören Metriken wie "Schritte im Vorfeld der Messung", "Zeit seit letzter Medikation" oder "Maximale Inaktivitätsdauer am Tag".
* **[F-06] Relationales Data Warehouse:** Das System schreibt transformierte Datenmodelle als klassisches Star-Schema (Faktentabellen und Dimensionstabellen) weg.
* **[F-07] Interaktive Analytik:** Es wird ein lokales Streamlit-Dashboard bereitgestellt, in dem Endnutzer die OLAP-Auswertungen dynamisch filtern und grafisch analysieren können.

---

## 2. Nicht-funktionale Anforderungen (Non-Functional Requirements)
*Diese Anforderungen definieren, **wie** das System aus Architektursicht agieren und beschaffen sein soll.*

* **[NF-01] Datenschutz und ethische Konformität:** Der Entwicklungsprozess nutzt echte, vom Entwickler freiwillig bereitgestellte und vollständig anonymisierte Gesundheitsdaten (Blutdruck und Smartwatch-Bewegungsprofile). Die finale Applikation dient der fachlichen Machbarkeitsprüfung im Rahmen der Projektarbeit, es werden keine Realdaten von Dritten verarbeitet.
* **[NF-02] Modularität (Separation of Concerns):** Die Pipeline-Bausteine (Extract, Transform, Load) werden softwaretechnisch so gekapselt, dass künftig neue Datenformate ergänzt werden können, ohne die bestehende Logik zu beschädigen.
* **[NF-03] Reproduzierbarkeit & Automatisierung:** Der gesamte ETL-End-to-End-Run muss über ein zentrales Steuer-Skript automatisiert und fehlerfrei gestartet werden können.
* **[NF-04] Portabilität:** Das Speichermedium des Data Warehouses ist dateibasiert (Vorschlag: SQLite oder DuckDB). Damit kann die Applikation "Out of the box" ohne komplexe Serverkomponenten lokal gestartet werden.
* **[NF-05] Erweiterbarkeit:** Das implementierte Star-Schema und die ETL-Pipeline müssen strukturell so ausgelegt sein, dass optionale Wetterdaten in einer späteren Phase per REST-API nahtlos hinzugefügt werden können.
