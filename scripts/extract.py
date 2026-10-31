import json
import os
from datetime import datetime
from pathlib import Path

import requests

CITY = os.environ.get("WEATHER_CITY", "Hyderabad")
API_KEY = os.environ.get("OPENWEATHER_API_KEY")

if not API_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY is not configured.")

PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

url = "https://api.openweathermap.org/data/2.5/weather"
response = requests.get(url, params={"q": CITY, "appid": API_KEY}, timeout=30)
response.raise_for_status()
weather_data = response.json()

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = RAW_DIR / f"raw_weather_{timestamp}.json"

with output_file.open("w", encoding="utf-8") as file:
    json.dump(weather_data, file, indent=4)

print(f"Raw weather data saved: {output_file}")
