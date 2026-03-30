# Anforderungen: Blutdruck-Überwachung

Dieses Dokument fasst die wesentlichen Systemanforderungen für das Data Engineering Projekt zusammen. Die Einstufung hilft dabei, den Scope der Projektarbeit präzise abzugrenzen.

## 1. Was das System können muss (Funktionale Anforderungen)

* **[F-01] Daten einlesen (ETL - Extract):** Das Programm muss Daten aus meiner Blutdruck-App (CSV) und von meiner Smartwatch (Google Takeout: JSON und CSV) laden können.
* **[F-02] Daten aufräumen:** Unterschiedliche Schreibweisen (z. B. beim Datum) müssen korrigiert werden, damit alles zusammenpasst.
* **[F-03] Zeiten anpassen:** Da nicht jede Sekunde gemessen wird, werden die Daten in Zeitblöcke (z. B. 15 oder 60 Minuten) zusammengefasst.
* **[F-04] Daten verknüpfen:** Blutdruck, Schritte und Medikamente müssen über die Patienten-Nummer und die Uhrzeit logisch zusammengeführt werden.
* **[F-05] Neue Werte berechnen:** Das System berechnet automatisch wichtige Infos, wie z. B. "Wie viele Schritte wurden vor der Messung gemacht?".
* **[F-06] Datenbank speichern (DWH):** Die fertigen Daten werden in einem sauberen **Star-Schema** (Haupt- und Detailtabellen) in einer Datenbank gespeichert.
* **[F-07] Auswertung (Dashboard):** Es gibt eine einfache Weboberfläche mit Streamlit, auf der man sich Diagramme anschauen und Filter benutzen kann.

---

## 2. Nicht-funktionale Anforderungen (Non-Functional Requirements)
*Diese Anforderungen definieren, **wie** das System aus Architektursicht agieren und beschaffen sein soll.*

* **[NF-01] Datenschutz:** Wir benutzen nur meine eigenen Daten, die vorher anonymisiert wurden. Es werden keine Daten von anderen Personen verarbeitet.
* **[NF-02] Baustein-Prinzip:** Das System ist so aufgebaut, dass man später leicht neue Datenquellen (z. B. eine neue App) hinzufügen kann, ohne alles umbauen zu müssen.
* **[NF-03] Automatisierung:** Der gesamte Ablauf (ETL) sollte per Knopfdruck oder über ein einziges Skript starten.
* **[NF-04] Technik:** Wir benutzen **Python 3** und eine kleine, einfache Datenbank (**SQLite3**). So braucht man keinen extra Server und kann alles direkt auf dem PC starten.
* **[NF-05] Spätere Erweiterung:** Der Aufbau (Star-Schema) soll so flexibel sein, dass man später auch Wetterdaten aus dem Internet hinzufügen könnte.
