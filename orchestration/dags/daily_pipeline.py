from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup

from ingest.jobs.daily_solar_job import run_solar_job
from ingest.jobs.daily_weather_job import run_weather_job

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=2),
    'execution_timeout': timedelta(minutes=30),
}

with DAG(
    dag_id='daily_pipeline',
    default_args=default_args,
    description='Daily solar and weather data ingestion followed by dbt transformations',
    schedule='0 2 * * *',  # 2:00 AM daily
    start_date=datetime(2026, 4, 1, tzinfo=None),
    catchup=False, 
    max_active_runs=1,
    tags=['ingestion', 'dbt', 'daily', 'production'],
    doc_md=__doc__,
) as dag:

    ingest_solar = PythonOperator(
        task_id='ingest_solar_data',
        python_callable=run_solar_job,
        op_kwargs={'target_timestamp': None}  
    )

    ingest_weather = PythonOperator(
        task_id='ingest_weather_data',
        python_callable=run_weather_job,
        op_kwargs={'target_date': None} 
    )

    with TaskGroup(group_id='dbt_transformations') as dbt_tasks:
        
        dbt_seed = BashOperator(
            task_id='dbt_seed',
            bash_command='cd /luminos && dbt seed --project-dir transform --profiles-dir transform --target prod',
            doc_md="Load WMO weather codes CSV into dim_weather_codes",
        )
        
        dbt_run = BashOperator(
            task_id='dbt_run',
            bash_command='cd /luminos && dbt run --project-dir transform --profiles-dir transform --target prod',
            doc_md="Execute all dbt models: staging → marts → reports",
        )
        
        dbt_test = BashOperator(
            task_id='dbt_test',
            bash_command='cd /luminos && dbt test --project-dir transform --profiles-dir transform --target prod',
            doc_md="Run dbt data quality tests",
        )

        dbt_seed >> dbt_run >> dbt_test

    [ingest_solar, ingest_weather] >> dbt_tasks