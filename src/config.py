from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "iot_db"

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
CSV_PATH = BASE_DIR / "data" / "temperature_readings.csv"
