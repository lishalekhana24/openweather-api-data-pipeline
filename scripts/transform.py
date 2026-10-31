import json
from datetime import datetime
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

raw_files = sorted(RAW_DIR.glob("raw_weather_*.json"))
if not raw_files:
    raise FileNotFoundError("No raw weather JSON file was found.")

with raw_files[-1].open("r", encoding="utf-8") as file:
    weather_data = json.load(file)

city = weather_data.get("name", "Unknown")
weather_items = weather_data.get("weather", [])
original_description = ""
if weather_items:
    original_description = weather_items[0].get("description", "") or ""

normalized_description = original_description.title() if original_description else "Unknown"
description = original_description.lower()

if "clear" in description:
    category = "Clear"
elif "cloud" in description:
    category = "Cloudy"
elif "rain" in description or "drizzle" in description:
    category = "Rainy"
else:
    category = "Other"

observation_time = weather_data.get("dt")
if observation_time is None:
    observation_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
else:
    observation_timestamp = datetime.fromtimestamp(observation_time).strftime("%Y-%m-%d %H:%M:%S")

df = pd.DataFrame([{
    "City": city,
    "Original Description": original_description if original_description else "Unknown",
    "Normalized Description": normalized_description,
    "Weather Category": category,
    "Observation Timestamp": observation_timestamp
}])

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = PROCESSED_DIR / f"transformed_weather_{timestamp}.csv"
df.to_csv(output_file, index=False)
print(df.to_string(index=False))
print(f"Transformed CSV saved: {output_file}")
