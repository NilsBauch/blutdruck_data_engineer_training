-- Stammdaten-Initialisierung

-- 1. Medikations-Katalog
INSERT INTO master_medications (name, dose_mg, description) VALUES 
('Ramipril', 2.5, 'ACE-Hemmer'),
('Ramipril', 5.0, 'ACE-Hemmer'),
('Ramipril', 10.0, 'ACE-Hemmer'),
('Candesartan', 4.0, 'Sartan (ARB)'),
('Candesartan', 8.0, 'Sartan (ARB)'),
('Candesartan', 16.0, 'Sartan (ARB)'),
('Candesartan', 32.0, 'Sartan (ARB)'),
('Bisoprolol', 1.25, 'Beta-Blocker'),
('Bisoprolol', 2.5, 'Beta-Blocker'),
('Bisoprolol', 5.0, 'Beta-Blocker'),
('Bisoprolol', 10.0, 'Beta-Blocker'),
('Amlodipin', 5.0, 'Calciumantagonist'),
('Amlodipin', 10.0, 'Calciumantagonist'),
('Metoprolol', 47.5, 'Beta-Blocker'),
('Metoprolol', 95.0, 'Beta-Blocker'),
('HCT', 12.5, 'Diuretikum'),
('HCT', 25.0, 'Diuretikum');

-- 2. Nutzerprofil (Patient 001)
-- Erfassung als Raucher, Bewegungstyp 'wenig', Alter 51, Geschlecht 'm'
INSERT INTO master_lifestyle (user_id, name, age, gender, is_smoker, movement_type, raw_data_folder) 
VALUES (1, 'Patient 001', 51, 'm', 1, 'wenig', 'patient_001');

-- 3. Medikationsplan für Patient 001
-- Verknüpfung mit Ramipril 5mg (ID 2 in obiger Liste)
-- Einnahme: morgens
INSERT INTO user_medication_plan (user_id, medication_id, time_of_day, is_active) 
VALUES (1, 2, 'morgens', 1);
