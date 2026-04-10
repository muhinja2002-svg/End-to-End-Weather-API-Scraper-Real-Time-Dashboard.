import os
import requests
import logging
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ValidationError

# --- CONFIG ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CITIES = ["Nairobi", "London", "Sydney", "Tokyo", "New York"]
SUPABASE_URL = "https://ahnotyrkehippbomgvop.supabase.co"
# These must be set in GitHub Secrets
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
OWM_API_KEY = os.environ.get("OWM_API_KEY")

class WeatherMetric(BaseModel):
    city: str
    temperature_c: float
    humidity_pct: int = Field(ge=0, le=100)
    status: str
    timestamp: datetime

def extract_from_api() -> list[dict]:
    records = []
    for city in CITIES:
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            resp = requests.get(url, params={
                "q": city,
                "appid": OWM_API_KEY,
                "units": "metric"
            }, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            records.append({
                "city": city,
                "temperature_c": data["main"]["temp"],
                "humidity_pct": data["main"]["humidity"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": data["weather"][0]["main"]
            })
            logger.info(f"Extracted: {city}")
        except Exception as e:
            logger.error(f"Failed to fetch {city}: {e}")
    return records

def load_to_supabase(data: list[dict]):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates" # FIX 2: Upsert logic
    }
    url = f"{SUPABASE_URL}/rest/v1/weather_metrics"
    
    validated_records = []
    for item in data:
        try:
            # FIX 3: Detailed validation logging
            record = WeatherMetric(**item)
            validated_records.append(record.model_dump(mode='json'))
        except ValidationError as e:
            logger.warning(f"Skipped invalid record for '{item.get('city', 'unknown')}': {e}")

    if validated_records:
        resp = requests.post(url, headers=headers, json=validated_records)
        resp.raise_for_status()
        logger.info(f"Successfully synced {len(validated_records)} records.")

if __name__ == "__main__":
    raw_data = extract_from_api()
    load_to_supabase(raw_data)