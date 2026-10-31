from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

required_columns = [
    "City",
    "Original Description",
    "Normalized Description",
    "Weather Category",
    "Observation Timestamp"
]

csv_files = sorted(PROCESSED_DIR.glob("transformed_weather_*.csv"))
if not csv_files:
    raise FileNotFoundError("No transformed weather CSV was found.")

df = pd.read_csv(csv_files[-1])

missing_columns = [column for column in required_columns if column not in df.columns]
if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

if df.empty:
    raise ValueError("CSV has no records.")

if df[required_columns].isnull().sum().sum() > 0:
    raise ValueError("CSV contains missing required values.")

allowed_categories = ["Clear", "Cloudy", "Rainy", "Other"]
if not df["Weather Category"].isin(allowed_categories).all():
    raise ValueError("CSV contains an invalid weather category.")

print("Validation successful!")
print(f"Validated file: {csv_files[-1]}")
print(f"Validated records: {len(df)}")
