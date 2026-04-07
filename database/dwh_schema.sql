-- ==========================================
-- Schema für das Data Warehouse (DWH)
-- Archiv: blutdruck_dwh.db
-- Fokus: Star-Schema (OLAP)
-- ==========================================

-- 1. Dimension: Nutzer
CREATE TABLE IF NOT EXISTS dim_user (
    user_id INTEGER PRIMARY KEY,
    gender VARCHAR(1),
    age INTEGER
);

-- 2. Dimension: Medikation
CREATE TABLE IF NOT EXISTS dim_medication (
    med_id INTEGER PRIMARY KEY,
    name TEXT,
    dosage_mg REAL,
    category TEXT,
    SCD_valid_from DATE DEFAULT '2000-01-01',
    SCD_valid_to DATE -- NULL = aktuell
);

-- 3. Dimension: Lifestyle
CREATE TABLE IF NOT EXISTS dim_lifestyle (
    lifestyle_id INTEGER PRIMARY KEY,
    is_smoker BOOLEAN,
    movement_type TEXT, -- 'wenig', 'mittel', 'sportlich'
    SCD_valid_from DATE DEFAULT '2000-01-01',
    SCD_valid_to DATE -- NULL = aktuell
);

-- 4. Dimension: Zeit/Datum
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
    user_id INTEGER,
    date_key INTEGER,
    time_key TEXT, -- Format: HH:MM
    med_id INTEGER,
    lifestyle_id INTEGER,
    
    -- Metriken
    systolic INTEGER,
    diastolic INTEGER,
    pulse INTEGER,
    steps_hourly INTEGER, -- Aggregiert oder anteilig
    weight_kg REAL,
    activity_minutes INTEGER,
    
    -- Berechnete Flags/Features für Analysen
    is_post_medication BOOLEAN,
    pulse_pressure INTEGER, -- Systolic - Diastolic 
    
    FOREIGN KEY (user_id) REFERENCES dim_user(user_id),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (med_id) REFERENCES dim_medication(med_id),
    FOREIGN KEY (lifestyle_id) REFERENCES dim_lifestyle(lifestyle_id)
);
