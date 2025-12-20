"""Minimal extract DAG placeholder."""
from datetime import datetime
from airflow import DAG

with DAG(dag_id="extract_dag", start_date=datetime(2025,1,1), schedule_interval="@hourly") as dag:
    pass
