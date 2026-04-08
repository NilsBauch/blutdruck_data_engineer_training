/*
 @licstart  The following is the entire license notice for the JavaScript code in this file.

 The MIT License (MIT)

 Copyright (C) 1997-2020 by Dimitri van Heesch

 Permission is hereby granted, free of charge, to any person obtaining a copy of this software
 and associated documentation files (the "Software"), to deal in the Software without restriction,
 including without limitation the rights to use, copy, modify, merge, publish, distribute,
 sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all copies or
 substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
 BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

 @licend  The above is the entire license notice for the JavaScript code in this file
*/
var NAVTREE =
[
  [ "Health Monitoring Data Pipeline", "index.html", [
    [ "Zentrale Dokumentation: Health Monitoring Data Pipeline", "index.html", "index" ],
    [ "Aktivitätsdiagramm (Whitebox): UC1 - Datenexporte im Raw-Ordner ablegen", "md__architektur_2_activity_2activity__diagram__uc1.html", null ],
    [ "Aktivitätsdiagramm (Whitebox): UC2 - ETL-Workflow ausführen", "md__architektur_2_activity_2activity__diagram__uc2.html", null ],
    [ "Aktivitätsdiagramm (Whitebox): UC3 - Daten transformieren &amp; in DWH integrieren", "md__architektur_2_activity_2activity__diagram__uc3.html", null ],
    [ "Aktivitätsdiagramm (Whitebox): UC4 - Dashboard starten", "md__architektur_2_activity_2activity__diagram__uc4.html", null ],
    [ "Aktivitätsdiagramm (Whitebox): UC5 - Analysen interaktiv filtern &amp; explorieren", "md__architektur_2_activity_2activity__diagram__uc5.html", null ],
    [ "Architektur-Übersicht: Health Monitoring Projekt", "md__architektur_2_architektur___uebersicht.html", [
      [ "1. Datenquellen und Formate", "md__architektur_2_architektur___uebersicht.html#autotoc_md7", null ],
      [ "2. Architekturdiagramm", "md__architektur_2_architektur___uebersicht.html#autotoc_md9", null ]
    ] ],
    [ "Datenbank- &amp; ETL-Übersicht", "md__architektur_2_datenbanken_2_datenbank___uebersicht.html", [
      [ "1. Datenfluss-Diagramm", "md__architektur_2_datenbanken_2_datenbank___uebersicht.html#autotoc_md11", null ],
      [ "2. Schichtenarchitektur", "md__architektur_2_datenbanken_2_datenbank___uebersicht.html#autotoc_md13", null ],
      [ "2. Staging Area (<span class=\"tt\">blutdruck_input.db</span>)", "md__architektur_2_datenbanken_2_datenbank___uebersicht.html#autotoc_md15", [
        [ "Stammdaten (Master Data)", "md__architektur_2_datenbanken_2_datenbank___uebersicht.html#autotoc_md16", null ],
        [ "Rohdaten-Tabellen (Raw Area)", "md__architektur_2_datenbanken_2_datenbank___uebersicht.html#autotoc_md17", null ]
      ] ],
      [ "3. ETL-Skripte &amp; Logik", "md__architektur_2_datenbanken_2_datenbank___uebersicht.html#autotoc_md19", null ],
      [ "4. Zielzustand: Warehouse (DWH)", "md__architektur_2_datenbanken_2_datenbank___uebersicht.html#autotoc_md21", [
        [ "Geplante Tabellen:", "md__architektur_2_datenbanken_2_datenbank___uebersicht.html#autotoc_md22", null ]
      ] ],
      [ "5. Speicherorte", "md__architektur_2_datenbanken_2_datenbank___uebersicht.html#autotoc_md24", null ]
    ] ],
    [ "Datenquellen-Verknüpfung und Struktur", "md__architektur_2_datenquellen___verknuepfung.html", [
      [ "1. Verzeichnisstruktur (Multi-User-Konzept)", "md__architektur_2_datenquellen___verknuepfung.html#autotoc_md26", [
        [ "Aufbau pro Patient:", "md__architektur_2_datenquellen___verknuepfung.html#autotoc_md27", null ]
      ] ],
      [ "2. Verknüpfungslogik", "md__architektur_2_datenquellen___verknuepfung.html#autotoc_md29", [
        [ "Ebene 1: Patienten-Zuordnung (Ordner-Ebene)", "md__architektur_2_datenquellen___verknuepfung.html#autotoc_md30", null ],
        [ "Ebene 2: Zeitliche Korrelation (Datensatz-Ebene)", "md__architektur_2_datenquellen___verknuepfung.html#autotoc_md31", null ]
      ] ],
      [ "3. Datenformate und SVD-Mapping", "md__architektur_2_datenquellen___verknuepfung.html#autotoc_md33", null ],
      [ "4. Erweiterbarkeit", "md__architektur_2_datenquellen___verknuepfung.html#autotoc_md35", null ]
    ] ],
    [ "Design-Dokumentation: Health Monitoring Plattform", "md__architektur_2_design_2_design___dokumentation.html", [
      [ "1. Zielsetzung des Projekts", "md__architektur_2_design_2_design___dokumentation.html#autotoc_md38", [
        [ "Die Fragen an die Daten:", "md__architektur_2_design_2_design___dokumentation.html#autotoc_md39", null ]
      ] ],
      [ "2. Der Dateneingang (Business-DB / Staging)", "md__architektur_2_design_2_design___dokumentation.html#autotoc_md41", [
        [ "Datenquellen (Übersicht)", "md__architektur_2_design_2_design___dokumentation.html#autotoc_md42", null ],
        [ "Ein Wort zum Speicherplatz (Kalkulation)", "md__architektur_2_design_2_design___dokumentation.html#autotoc_md43", null ],
        [ "Datenbank-Design (Normalform)", "md__architektur_2_design_2_design___dokumentation.html#autotoc_md44", null ],
        [ "Datenmodell (ERM)", "md__architektur_2_design_2_design___dokumentation.html#autotoc_md45", null ]
      ] ],
      [ "3. Der Auswertungs-Bereich (Data Warehouse)", "md__architektur_2_design_2_design___dokumentation.html#autotoc_md47", [
        [ "Wie das funktioniert:", "md__architektur_2_design_2_design___dokumentation.html#autotoc_md48", null ],
        [ "Star-Schema Modell (mER)", "md__architektur_2_design_2_design___dokumentation.html#autotoc_md49", null ]
      ] ],
      [ "4. Wie kommen die Daten rüber? (ETL &amp; Mapping)", "md__architektur_2_design_2_design___dokumentation.html#autotoc_md51", [
        [ "ETL Mapping Tabelle (Detailliert)", "md__architektur_2_design_2_design___dokumentation.html#autotoc_md52", null ]
      ] ],
      [ "5. Historie bewahren (SCD 2)", "md__architektur_2_design_2_design___dokumentation.html#autotoc_md54", [
        [ "Technische Spalten:", "md__architektur_2_design_2_design___dokumentation.html#autotoc_md55", null ]
      ] ],
      [ "Anhang: Technische Modelle (Mermaid)", "md__architektur_2_design_2_design___dokumentation.html#autotoc_md57", [
        [ "ERM (Business-DB)", "md__architektur_2_design_2_design___dokumentation.html#autotoc_md58", null ],
        [ "mER (Star-Schema)", "md__architektur_2_design_2_design___dokumentation.html#autotoc_md59", null ]
      ] ]
    ] ],
    [ "Use-Case-Diagramm: Health Monitoring (Blutdruck &amp; Aktivität)", "md__architektur_2_use_case_2use__case__diagram.html", [
      [ "1. Übersicht der Akteure", "md__architektur_2_use_case_2use__case__diagram.html#autotoc_md61", null ],
      [ "2. UML Use-Case Diagramm", "md__architektur_2_use_case_2use__case__diagram.html#autotoc_md63", null ],
      [ "3. Beschreibung der Anwendungsfälle (Use-Cases)", "md__architektur_2_use_case_2use__case__diagram.html#autotoc_md65", null ]
    ] ],
    [ "Projektidee: Health Monitoring", "md__aufgabenstellung_2_idee.html", [
      [ "Die Idee", "md__aufgabenstellung_2_idee.html#autotoc_md67", null ],
      [ "Anforderungen der Projektarbeit", "md__aufgabenstellung_2_idee.html#autotoc_md69", null ],
      [ "Woher kommen die Daten?", "md__aufgabenstellung_2_idee.html#autotoc_md71", [
        [ "1. Blutdruck-Werte", "md__aufgabenstellung_2_idee.html#autotoc_md72", null ],
        [ "2. Schritte und Aktivität", "md__aufgabenstellung_2_idee.html#autotoc_md73", null ],
        [ "3. Medikamente", "md__aufgabenstellung_2_idee.html#autotoc_md74", null ],
        [ "4. Vielleicht später: Wetterdaten", "md__aufgabenstellung_2_idee.html#autotoc_md75", null ]
      ] ],
      [ "Welche Fragen sollen beantwortet werden? (OLAP-Analyse)", "md__aufgabenstellung_2_idee.html#autotoc_md77", [
        [ "Hilft Bewegung dem Blutdruck?", "md__aufgabenstellung_2_idee.html#autotoc_md78", null ],
        [ "Wie gut wirken die Medikamente?", "md__aufgabenstellung_2_idee.html#autotoc_md79", null ],
        [ "Bewegung und Medikamente zusammen", "md__aufgabenstellung_2_idee.html#autotoc_md80", null ],
        [ "Warnsignale erkennen", "md__aufgabenstellung_2_idee.html#autotoc_md81", null ]
      ] ],
      [ "Technik im Hintergrund (ETL &amp; DWH)", "md__aufgabenstellung_2_idee.html#autotoc_md83", [
        [ "1. Daten einsammeln (Extract)", "md__aufgabenstellung_2_idee.html#autotoc_md84", null ],
        [ "2. Daten aufbereiten (Transform)", "md__aufgabenstellung_2_idee.html#autotoc_md85", null ],
        [ "3. Daten speichern (Load)", "md__aufgabenstellung_2_idee.html#autotoc_md86", null ],
        [ "4. Anzeigen der Ergebnisse (Visualisierung)", "md__aufgabenstellung_2_idee.html#autotoc_md87", null ]
      ] ],
      [ "Datenschutz", "md__aufgabenstellung_2_idee.html#autotoc_md89", null ]
    ] ],
    [ "Projektidee: Health Monitoring für ältere Menschen", "md__r_e_a_d_m_e.html", [
      [ "Kernidee", "md__r_e_a_d_m_e.html#autotoc_md96", null ],
      [ "Formale Anforderungen der Projektarbeit", "md__r_e_a_d_m_e.html#autotoc_md98", null ],
      [ "Datenquellen und Schnittstellen", "md__r_e_a_d_m_e.html#autotoc_md100", [
        [ "1. Kardiovaskuläre Daten (Blutdruck)", "md__r_e_a_d_m_e.html#autotoc_md101", null ],
        [ "2. Bewegungs- und Aktivitätsdaten", "md__r_e_a_d_m_e.html#autotoc_md102", null ],
        [ "3. Medikationshistorie", "md__r_e_a_d_m_e.html#autotoc_md103", null ],
        [ "4. Optionale Erweiterung: Wetterdaten", "md__r_e_a_d_m_e.html#autotoc_md104", null ]
      ] ],
      [ "Geplante OLAP-Analysen und Fragestellungen", "md__r_e_a_d_m_e.html#autotoc_md106", [
        [ "Einfluss der Bewegung auf den Blutdruck", "md__r_e_a_d_m_e.html#autotoc_md107", null ],
        [ "Einfluss der Medikation auf den Blutdruck", "md__r_e_a_d_m_e.html#autotoc_md108", null ],
        [ "Kombinierte Faktoren (Bewegung und Medikation)", "md__r_e_a_d_m_e.html#autotoc_md109", null ],
        [ "Präventives Monitoring (Sturz- und Gefahrenanalyse)", "md__r_e_a_d_m_e.html#autotoc_md110", null ]
      ] ],
      [ "Grobe technische Architektur (ETL &amp; DWH)", "md__r_e_a_d_m_e.html#autotoc_md112", [
        [ "1. Extract", "md__r_e_a_d_m_e.html#autotoc_md113", null ],
        [ "2. Transform", "md__r_e_a_d_m_e.html#autotoc_md114", null ],
        [ "3. Load", "md__r_e_a_d_m_e.html#autotoc_md115", null ],
        [ "4. Visualisierung &amp; Analyse", "md__r_e_a_d_m_e.html#autotoc_md116", null ],
        [ "Dashboard starten:", "md__r_e_a_d_m_e.html#autotoc_md117", null ],
        [ "Beantwortete Forschungsfragen:", "md__r_e_a_d_m_e.html#autotoc_md118", null ]
      ] ],
      [ "Datenschutz und Ethik", "md__r_e_a_d_m_e.html#autotoc_md120", null ]
    ] ],
    [ "Anforderungen: Blutdruck-Überwachung", "md__requirements_2requirements.html", [
      [ "1. Was das System können muss (Funktionale Anforderungen)", "md__requirements_2requirements.html#autotoc_md122", null ],
      [ "2. Nicht-funktionale Anforderungen (Non-Functional Requirements)", "md__requirements_2requirements.html#autotoc_md124", null ]
    ] ],
    [ "Pakete", "namespaces.html", [
      [ "Paket-Liste", "namespaces.html", "namespaces_dup" ],
      [ "Paketelemente", "namespacemembers.html", [
        [ "Alle", "namespacemembers.html", null ],
        [ "Funktionen", "namespacemembers_func.html", null ],
        [ "Variablen", "namespacemembers_vars.html", null ]
      ] ]
    ] ],
    [ "Dateien", "files.html", [
      [ "Auflistung der Dateien", "files.html", "files_dup" ]
    ] ]
  ] ]
];

var NAVTREEINDEX =
[
"app_8py.html"
];

var SYNCONMSG = 'Klicken um Panelsynchronisation auszuschalten';
var SYNCOFFMSG = 'Klicken um Panelsynchronisation einzuschalten';
var LISTOFALLMEMBERS = 'Aufstellung aller Elemente';