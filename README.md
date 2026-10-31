# OpenWeather API Data Pipeline

A beginner-friendly weather data pipeline built with Python and Apache Airflow on AWS EC2.

## Project workflow

1. **Extract:** Fetch current weather for Hyderabad using the OpenWeather API and save a timestamped raw JSON file.
2. **Transform:** Normalize the weather description and classify it as `Clear`, `Cloudy`, `Rainy`, or `Other`.
3. **Validate:** Check the required CSV columns, non-empty output, missing values, and allowed categories.
4. **Email:** Send a Gmail success notification only after validation succeeds.

## Required CSV columns

- City
- Original Description
- Normalized Description
- Weather Category
- Observation Timestamp

## Repository structure

```text
OpenWeather_Project/
├── dags/
│   └── openweather_dag.py
├── scripts/
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   └── send_email.py
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── OpenWeather_Assessment.ipynb
├── evidence/
├── requirements.txt
└── README.md
```

## Notebook

The original Jupyter Notebook used during development is included in `notebooks/`.
Its code cells are retained; cell outputs are cleared before sharing so personal
email addresses and old runtime output are not published. The email cell includes
the missing `EmailMessage` construction required by `send_message`.

## Airflow setup on EC2

The Airflow DAG reads secrets from Airflow Variables. Configure these Variables
in the Airflow environment before triggering the DAG:

- `OPENWEATHER_API_KEY`
- `WEATHER_CITY` (set to `Hyderabad`)
- `GMAIL_SENDER`
- `GMAIL_RECEIVER`
- `GMAIL_APP_PASSWORD`

Do not put API keys, Gmail app passwords, or other secrets in this repository.

Place this project's `dags/` folder in the Airflow DAGs folder, and keep the
`scripts/` and `data/` folders at the project root as shown. The DAG uses the
Python environment running Airflow to execute each script.

## Run

```bash
python -m pip install requests pandas
```

Trigger `openweather_pipeline` manually from the Airflow UI. The tasks run in
this order: `extract → transform → validate → email`. A failure stops downstream
tasks, so the success email is sent only after validation succeeds.

## Evidence to add

Add screenshots to `evidence/` showing:
- Airflow DAG Graph with all four tasks successful
- Task logs
- Raw JSON file
- Transformed CSV with the five required columns
- Received success email

## Security

The notebook's outputs have been cleared. Never commit `.env` files, API keys,
Gmail app passwords, or other credentials.
