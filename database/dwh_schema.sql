-- @file dwh_schema.sql
-- @brief Definition des Star-Schemas für das Data Warehouse.
--
-- Dieses Schema beinhaltet die Faktentabelle für Gesundheitsmetriken sowie 
-- Dimensionstabellen für Nutzer, Medikation (SCD 2) und Lifestyle (SCD 2).
--
-- @section Architecture Schichtenmodell
-- - **Dimensionen**: dim_user, dim_medication, dim_lifestyle, dim_date
-- - **Fakten**: fact_health_metrics

-- 1. Dimension: Nutzer (Stammdaten)
CREATE TABLE IF NOT EXISTS dim_user (
    user_id INTEGER PRIMARY KEY, -- Business Key
    gender VARCHAR(1),
    age INTEGER
);

-- 2. Dimension: Medikation (SCD Type 2)
CREATE TABLE IF NOT EXISTS dim_medication (
    med_key INTEGER PRIMARY KEY AUTOINCREMENT, -- Surrogate Key
    med_id INTEGER, -- Business Key
    name TEXT,
    dosage_mg REAL,
    category TEXT,
    SCD_valid_from DATE DEFAULT '2000-01-01',
    SCD_valid_to DATE DEFAULT '9999-12-31'
);

-- 3. Dimension: Lifestyle (SCD Type 2)
CREATE TABLE IF NOT EXISTS dim_lifestyle (
    lifestyle_key INTEGER PRIMARY KEY AUTOINCREMENT, -- Surrogate Key
    user_id INTEGER, -- Business Key
    is_smoker BOOLEAN,
    movement_type TEXT, -- 'wenig', 'mittel', 'sportlich'
    SCD_valid_from DATE DEFAULT '2000-01-01',
    SCD_valid_to DATE DEFAULT '9999-12-31'
);

-- 4. Dimension: Zeit/Datum (Stammdaten)
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY, -- Format: YYYYMMDD
    full_date DATE,
    day INTEGER,
    month INTEGER,
    year INTEGER,
    day_name TEXT,
    is_weekend BOOLEAN
);

-- 5. Faktentabelle: Gesundheitsmetriken
-- Verknüpft alle Dimensionen mit den eigentlichen Messwerten
CREATE TABLE IF NOT EXISTS fact_health_metrics (
    fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,      -- Business Key (für Triage)
    date_key INTEGER,     -- FK zu dim_date
    time_key TEXT,        -- Format: HH:MM
    med_key INTEGER,      -- FK zu dim_medication (Surrogate Key)
    lifestyle_key INTEGER, -- FK zu dim_lifestyle (Surrogate Key)
    
    -- Metriken
    systolic INTEGER,
    diastolic INTEGER,
    pulse INTEGER,
    steps_hourly INTEGER, 
    weight_kg REAL,
    activity_minutes INTEGER,
    
    -- Berechnete Flags/Features
    is_post_medication BOOLEAN,
    pulse_pressure INTEGER, 
    
    -- Audit-Felder
    load_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES dim_user(user_id),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (med_key) REFERENCES dim_medication(med_key),
    FOREIGN KEY (lifestyle_key) REFERENCES dim_lifestyle(lifestyle_key),
    
    -- Dublettenprüfung: Ein Messwert pro User/Tag/Uhrzeit
    UNIQUE(user_id, date_key, time_key)
);
