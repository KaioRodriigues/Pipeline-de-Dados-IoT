CREATE TABLE IF NOT EXISTS temperature_readings (
    id SERIAL PRIMARY KEY,
    device_id TEXT,
    timestamp TIMESTAMP,
    temperature DOUBLE PRECISION,
    location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
