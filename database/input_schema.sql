-- Schema für blutdruck_input.db

-- 1. Stammdaten: Medikamente
CREATE TABLE IF NOT EXISTS master_medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    dose_mg REAL NOT NULL,
    description TEXT
);

-- 2. Stammdaten: Lifestyle & Profile
CREATE TABLE IF NOT EXISTS master_lifestyle (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    is_smoker BOOLEAN DEFAULT 0,
    movement_type TEXT, -- 'wenig', 'mittel', 'sportlich'
    raw_data_folder TEXT -- Name des Unterverzeichnisses in data/01_raw/
);

-- 3. Verknüpfung: Medikationsplan pro Nutzer
CREATE TABLE IF NOT EXISTS user_medication_plan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    medication_id INTEGER NOT NULL,
    time_of_day TEXT, -- 'morgens', 'mittags', 'abends', 'nachts'
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES master_lifestyle(user_id),
    FOREIGN KEY (medication_id) REFERENCES master_medications(id)
);

-- 4. Rohdaten: Blutdruck (SVD) aus App
CREATE TABLE IF NOT EXISTS raw_blood_pressure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL, -- ISO-Format YYYY-MM-DD HH:MM:SS
    systolic INTEGER,
    diastolic INTEGER,
    pulse INTEGER,
    is_manual BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES master_lifestyle(user_id)
);

-- 5. Rohdaten: Aktivität & Körper aus Smartwatch
CREATE TABLE IF NOT EXISTS raw_activity_daily (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL, -- ISO YYYY-MM-DD
    steps INTEGER,
    activity_minutes INTEGER,
    weight_kg REAL,
    FOREIGN KEY (user_id) REFERENCES master_lifestyle(user_id)
);
