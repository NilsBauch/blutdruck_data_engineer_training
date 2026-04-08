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

-- 2. Nutzer-Platzhalter (Wird durch ETL aus JSON überschrieben/erstellt)
-- Die Initialisierung erfolgt nun primär über data/01_raw/*/profile/user_profile.json
