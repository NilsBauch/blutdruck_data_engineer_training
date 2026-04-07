# Projektidee: Health Monitoring
Fokus: Blutdruck, Bewegung & Medikamente

## Die Idee
Ich möchte ein System bauen, das verschiedene Gesundheitsdaten zusammenführt und auswertet. Es geht vor allem um diese Punkte:

- Wie hat sich der Blutdruck entwickelt?
- Wie viel hat sich die Person bewegt (Schritte)?
- Wann wurden welche Medikamente genommen?

Das Ziel ist es, herauszufinden, wie Bewegung, die Tageszeit und Medikamente den Blutdruck beeinflussen. Außerdem möchte ich schauen, ob man Warnzeichen automatisch erkennen kann – zum Beispiel, wenn der Blutdruck hoch bleibt, obwohl sich die Person kaum bewegt.

---

## Anforderungen der Projektarbeit
Das Projekt erfüllt die offiziellen Vorgaben:

> "Die Daten sollen aus mindestens drei unterschiedlichen Quellen stammen (z. B. CSV, JSON, Excel/XLSX, Datenbanken, REST APIs oder Open Data Portale)."

> "Die Ergebnisse der OLAP-Analysen werden anschließend in einem Streamlit-Dashboard visualisiert."

---

## Woher kommen die Daten?

### 1. Blutdruck-Werte
- Das sind echte Messwerte von mir, die ich anonymisiert habe.
- Ich exportiere sie als CSV-Datei aus meiner Blutdruck-App.

### 2. Schritte und Aktivität
- Diese Daten kommen von meiner Smartwatch (über Google Takeout).
- Die Daten liegen als JSON oder CSV vor und sind ebenfalls anonymisiert.

### 3. Medikamente
- Eine Excel- oder CSV-Liste, in der steht, wann was genommen wurde.
- Wichtige Infos: Welches Medikament, wie viel (mg) und wie spät es bei der Einnahme war.

### 4. Vielleicht später: Wetterdaten
- Ich könnte über eine API noch Wetterdaten (Temperatur, Luftdruck) abrufen.
- Die Frage ist: Hat das Wetter auch einen Einfluss auf den Blutdruck?

---

## Welche Fragen sollen beantwortet werden? (OLAP-Analyse)

### Hilft Bewegung dem Blutdruck?
- Ich vergleiche den Blutdruck an Tagen mit viel Bewegung mit Tagen, an denen man faul war.
- Gibt es Tageszeiten, an denen der Blutdruck trotz Sport nicht sinkt?

### Wie gut wirken die Medikamente?
- Wie verändert sich der Blutdruck in den ersten Stunden nach der Tablette?
- Wirken unterschiedliche Medikamente auch unterschiedlich stark?

### Bewegung und Medikamente zusammen
- Hilft Sport direkt nach der Tabletteneinnahme dabei, den Blutdruck besser zu senken?
- Gibt es Momente, in denen beides (Sport + Medikamente) nicht ausreicht?

### Warnsignale erkennen
- Wenn sich jemand ungewöhnlich lange gar nicht bewegt, könnte das ein Sturz sein.
- Ein Alarm könnte ausgelöst werden, wenn jemand seine Tabletten vergessen hat, der Blutdruck hoch ist und er sich nicht bewegt.

---

## Technik im Hintergrund (ETL & DWH)

### 1. Daten einsammeln (Extract)
- CSV- und Excel-Dateien einlesen.
- JSON-Daten von der Smartwatch verarbeiten.

### 2. Daten aufbereiten (Transform)
- Die Zeiten vereinheitlichen (z. B. alles auf 15-Minuten-Blöcke zusammenfassen).
- Die Daten über die Patienten-ID und die Zeit miteinander verknüpfen.
- Neue Werte berechnen (z. B. "Wie lange ist die letzte Tablette her?").

### 3. Daten speichern (Load)
- **Data Warehouse (Star-Schema)**:
  - Eine Haupttabelle für alle Messwerte.
  - Zusatztabellen für Details zu Patienten, Zeit, Medikamenten und Aktivitäten.

### 4. Anzeigen der Ergebnisse (Visualisierung)
- Eine App mit Streamlit bauen.
- Dort kann man sich Diagramme anschauen und die Daten filtern.

---

## Datenschutz
Da es um Gesundheitsdaten geht, passe ich besonders auf:
- Ich benutze nur meine eigenen Daten und mache sie komplett anonym.
- Das Projekt ist eine technische Übung und keine echte medizinische Beratung.
