FROM apache/airflow:3.2.0

RUN pip install --no-cache-dir \
    "dbt-core>=1.11.6" \
    "dbt-duckdb>=1.10.1" \
    "duckdb>=1.4.4" \
    "numpy>=2.2.6" \
    "openmeteo-requests>=1.7.5" \
    "pandas>=2.3.3" \
    "requests>=2.32.5" \
    "requests-cache>=1.3.0" \
    "retry-requests>=2.0.0" \
    "python-dotenv>=1.0.0"