import json
import sqlite3
import logging
from pydantic import ValidationError
from models import WeatherRecord

# Configure robust logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DB_PATH = 'data/weather.db'

def setup_database():
    """Creates the database with a UNIQUE constraint for idempotency."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS weather_logs (
                city TEXT,
                temperature_c REAL,
                humidity_pct INTEGER,
                timestamp TEXT,
                status TEXT,
                UNIQUE(city, timestamp) -- Green Flag: Prevents duplicate inserts
            )
        """)

def extract_data() -> list:
    """Simulates extracting data from an API."""
    try:
        with open('data/raw_mock_api.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Raw data file not found. Did you run generate_mock_data.py?")
        return []

def process_and_load(raw_data: list):
    setup_database()
    valid_records = 0
    errors = 0

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for item in raw_data:
            try:
                # 1. Validate Data (The Data Contract)
                record = WeatherRecord(**item)
                
                # 2. Idempotent Load (UPSERT logic via IGNORE)
                cursor.execute("""
                    INSERT OR IGNORE INTO weather_logs 
                    (city, temperature_c, humidity_pct, timestamp, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (record.city, record.temperature_c, record.humidity_pct, 
                      record.timestamp.isoformat(), record.status))
                
                if cursor.rowcount > 0:
                    valid_records += 1

            except ValidationError as e:
                logger.warning(f"Data Schema Drift/Validation Error for {item.get('city')}: {e.errors()[0]['msg']}")
                errors += 1
            except Exception as e:
                logger.critical(f"Unexpected system failure: {str(e)}")
                errors += 1
        
        conn.commit()
    logger.info(f"Pipeline finished. Inserted: {valid_records} | Dropped/Skipped: {errors}")

if __name__ == "__main__":
    logger.info("Starting ETL Pipeline...")
    data = extract_data()
    process_and_load(data)