CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT
    device_id,
    AVG(temperature) AS avg_temp
FROM temperature_readings
GROUP BY device_id;

CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    EXTRACT(HOUR FROM timestamp)::INT AS hora,
    COUNT(*) AS total_leituras
FROM temperature_readings
GROUP BY hora;

CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT
    DATE(timestamp) AS dia,
    MAX(temperature) AS temp_max,
    MIN(temperature) AS temp_min
FROM temperature_readings
GROUP BY dia;

CREATE OR REPLACE VIEW leituras_por_localizacao AS
SELECT
    location,
    COUNT(*) AS total_leituras
FROM temperature_readings
GROUP BY location;
