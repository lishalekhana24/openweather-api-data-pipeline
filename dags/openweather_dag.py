from datetime import datetime, timedelta
from pathlib import Path
import os
import subprocess
import sys

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator

PROJECT_DIR = Path(os.environ.get("OPENWEATHER_PROJECT_DIR", "/home/ubuntu/OpenWeather_Project"))

def run_script(script_name):
    env = os.environ.copy()
    env["OPENWEATHER_API_KEY"] = Variable.get("OPENWEATHER_API_KEY")
    env["WEATHER_CITY"] = Variable.get("WEATHER_CITY", default_var="Hyderabad")
    env["GMAIL_SENDER"] = Variable.get("GMAIL_SENDER")
    env["GMAIL_RECEIVER"] = Variable.get("GMAIL_RECEIVER")
    env["GMAIL_APP_PASSWORD"] = Variable.get("GMAIL_APP_PASSWORD")

    script_path = PROJECT_DIR / "scripts" / script_name
    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(PROJECT_DIR),
        env=env,
        check=True
    )

def extract():
    run_script("extract.py")

def transform():
    run_script("transform.py")

def validate():
    run_script("validate.py")

def send_email():
    run_script("send_email.py")

with DAG(
    dag_id="openweather_pipeline",
    description="Hyderabad weather extraction, transformation, validation and email",
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
    default_args={
        "owner": "openweather",
        "retries": 1,
        "retry_delay": timedelta(minutes=1)
    },
    tags=["openweather", "weather", "assessment"]
) as dag:
    extract_task = PythonOperator(task_id="extract", python_callable=extract)
    transform_task = PythonOperator(task_id="transform", python_callable=transform)
    validate_task = PythonOperator(task_id="validate", python_callable=validate)
    email_task = PythonOperator(task_id="email", python_callable=send_email)

    extract_task >> transform_task >> validate_task >> email_task
