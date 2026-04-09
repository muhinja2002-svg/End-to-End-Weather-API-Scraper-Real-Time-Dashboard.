import json
import random
from datetime import datetime, timedelta
import os

def generate_weather_data(num_records=50):
    cities = ["New York", "London", "Tokyo", "Nairobi", "Sydney"]
    data = []
    base_time = datetime.now()

    for i in range(num_records):
        # Introduce a deliberate null occasionally to test our data empathy/validation
        temp = round(random.uniform(-10.0, 40.0), 2) if random.random() > 0.05 else None
        
        record = {
            "city": random.choice(cities),
            "temperature_c": temp,
            "humidity_pct": random.randint(30, 95),
            "timestamp": (base_time - timedelta(minutes=i*15)).isoformat(),
            "status": random.choice(["Clear", "Rain", "Cloudy", "Storm"])
        }
        data.append(record)

    os.makedirs('data', exist_ok=True)
    with open('data/raw_mock_api.json', 'w') as f:
        json.dump(data, f, indent=4)
    print(f"✅ Generated {num_records} synthetic records in data/raw_mock_api.json")

if __name__ == "__main__":
    generate_weather_data()