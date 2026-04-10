import os
import json
import logging
import requests
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ValidationError

# 1. SETUP & LOGGING
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 2. CONFIGURATION
SUPABASE_URL = "https://ahnotyrkehippbomgvop.supabase.co"
TABLE_NAME = "weather_metrics"
RAW_DATA_PATH = "data/raw_mock_api.json"

# --- SMART KEY MANAGEMENT ---
# This looks for the "SUPABASE_KEY" secret in GitHub Actions.
# If it doesn't find it, it falls back to your manual key for local testing.
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_3bOU_ULwZFEHKac3zkHsPg_Fw2WhCRM")

# 3. DATA SCHEMA
class WeatherData(BaseModel):
    city: str
    temperature_c: Optional[float] = 0.0
    humidity_pct: Optional[int] = 0
    timestamp: datetime
    status: str

# 4. ETL FUNCTIONS
def extract_data() -> List[dict]:
    """Reads raw JSON data from the local file."""
    try:
        with open(RAW_DATA_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Source file not found at {RAW_DATA_PATH}")
        return []

def process_and_load_via_api(raw_data: List[dict]):
    """Validates and pushes data using HTTPS API."""
    valid_records = []
    
    for item in raw_data:
        try:
            record = WeatherData(**item)
            data_dict = record.model_dump()
            # Convert timestamp to ISO format string for the API
            data_dict['timestamp'] = data_dict['timestamp'].isoformat()
            valid_records.append(data_dict)
        except ValidationError:
            continue

    if valid_records:
        # Standard HTTPS headers for Supabase PostgREST
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}"
        
        try:
            response = requests.post(url, headers=headers, json=valid_records)
            
            if response.status_code in [200, 201]:
                logger.info(f"🚀 SUCCESS: Uploaded {len(valid_records)} rows to Supabase Cloud!")
            else:
                logger.error(f"❌ API ERROR: {response.status_code} - {response.text}")
        except Exception as e:
            logger.critical(f"❌ CONNECTION ERROR: {str(e)}")
    else:
        logger.error("No valid records found to process.")

# 5. EXECUTION
if __name__ == "__main__":
    logger.info("Starting Automated ETL Pipeline...")
    data = extract_data()
    if data:
        process_and_load_via_api(data)