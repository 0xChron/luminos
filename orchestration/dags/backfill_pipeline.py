from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.exceptions import AirflowException

from ingest.jobs.backfill_solar_job import run_backfill_solar_job
from ingest.jobs.backfill_weather_job import run_backfill_weather_job


def validate_backfill_params(**context):
    conf = context['dag_run'].conf or {}
    
    if 'start_date' not in conf or 'end_date' not in conf:
        raise AirflowException(
            "Missing required parameters. Trigger with:\n"
            "airflow dags trigger backfill_pipeline --conf "
            "'{\"start_date\": \"2026-04-01\", \"end_date\": \"2026-04-15\"}'"
        )
    
    try:
        start = datetime.strptime(conf['start_date'], '%Y-%m-%d')
        end = datetime.strptime(conf['end_date'], '%Y-%m-%d')
        
        if start > end:
            raise AirflowException(f"start_date must be <= end_date")
            
        if end > datetime.now():
            raise AirflowException("Cannot backfill future dates")
            
    except ValueError as e:
        raise AirflowException(f"Invalid date format. Use YYYY-MM-DD: {e}")
    
    print(f"✓ Validation passed: {conf['start_date']} to {conf['end_date']}")
    return True


# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2),
}

# DAG definition
with DAG(
    dag_id='backfill_pipeline',
    default_args=default_args,
    description='Manual backfill pipeline for solar and weather data with date range parameters',
    schedule=None,  # Manual trigger only
    start_date=datetime(2026, 4, 1, tzinfo=None),
    catchup=False,
    max_active_runs=1,
    tags=['backfill', 'manual', 'ingestion', 'dbt']
) as dag:

    validate = PythonOperator(
        task_id='validate_parameters',
        python_callable=validate_backfill_params,
    )

    backfill_solar = PythonOperator(
        task_id='backfill_solar_data',
        python_callable=run_backfill_solar_job,
        op_kwargs={
            'start_date': '{{ dag_run.conf.get("start_date") }}',
            'end_date': '{{ dag_run.conf.get("end_date") }}'
        }
    )

    backfill_weather = PythonOperator(
        task_id='backfill_weather_data',
        python_callable=run_backfill_weather_job,
        op_kwargs={
            'start_date': '{{ dag_run.conf.get("start_date") }}',
            'end_date': '{{ dag_run.conf.get("end_date") }}'
        }
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

    validate >> [backfill_solar, backfill_weather] >> dbt_tasks