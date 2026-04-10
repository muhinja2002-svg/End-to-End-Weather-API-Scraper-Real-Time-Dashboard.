-- Schema for Weather Analytics Platform
-- This ensures data integrity and prevents duplicates during hourly syncs

CREATE TABLE IF NOT EXISTS weather_metrics (
    id          BIGSERIAL PRIMARY KEY,
    city        TEXT NOT NULL,
    temperature_c FLOAT,
    humidity_pct  INT,
    timestamp   TIMESTAMPTZ NOT NULL,
    status      TEXT,
    CONSTRAINT unique_city_timestamp UNIQUE (city, timestamp)
);

-- Indexes for optimized dashboard performance
CREATE INDEX IF NOT EXISTS idx_weather_timestamp ON weather_metrics (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_weather_city ON weather_metrics (city);