"""Minimal transform DAG placeholder."""
from datetime import datetime
from airflow import DAG

with DAG(dag_id="transform_dag", start_date=datetime(2025,1,1), schedule_interval="@daily") as dag:
    pass
