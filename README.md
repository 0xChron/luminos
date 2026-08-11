# Luminos

**Luminos** is an automated data platform that ingests solar energy metrics and weather data, transforms them into analytics-ready datasets, and supports monitoring and forecasting of solar energy performance.

If you're interested in residential solar energy generation data, I've made my dataset public. You can access it here:

[Solar Energy Generation and Weather Data](https://www.kaggle.com/datasets/christiancanillas/solar-energy-generation-and-weather-data)

## Architecture

![Luminos system architecture](assets/images/system-architecture.jpg)

## Data Lineage

![Luminos data lineage](assets/images/data-lineage.jpg)

## Features

- **Automated daily ingestion**: Scheduled data collection at 2 AM GMT+8
- **Historical backfilling**: Flexible date-range backfill
- **Data quality tests**: Automated validation via dbt tests
- **Multi-grain analysis**: 5-minute raw → hourly → daily → monthly aggregations

## Project Structure
```
luminos/
├── .env.example                # Template for environment variables
├── docker-compose.yaml         # Airflow services configuration
├── pyproject.toml              # Python dependencies
├── README.md                   # This file
│
├── ingest/                     # Data ingestion layer
│   ├── client/                 # API clients
│   │   ├── deye_api.py         # Deye Cloud API client
│   │   └── openmeteo_api.py    # Open-Meteo API client
│   ├── extract/                # Data extractors
│   │   ├── solar.py            # Solar data extraction & transformation
│   │   └── weather.py          # Weather data extraction & transformation
│   ├── jobs/                   # Airflow job definitions
│   │   ├── daily_solar_job.py
│   │   ├── daily_weather_job.py
│   │   ├── backfill_solar_job.py
│   │   └── backfill_weather_job.py
│   ├── load/                   # Data loaders
│   │   └── duckdb_loader.py    # DuckDB loading logic
│   ├── utils/
│   │   ├── dates.py
│   │   └── logging.py
│   └── config.py               # Configuration management
│
├── transform/                  # dbt transformation layer
│   ├── dbt_project.yml
│   ├── profiles.yml            # DuckDB/MotherDuck connection config
│   ├── models/
│   │   ├── staging/            # Type casting & cleaning (views)
│   │   ├── marts/              # Core dimensional model (tables)
│   │   │   ├── dimensions/     # dim_date, dim_weather_codes
│   │   │   └── facts/          # Solar & weather facts
│   │   └── reports/            # Analysis-ready views (OBTs)
│   └── seeds/
│       └── wmo_weather_codes.csv
│
└── orchestration/              # Airflow orchestration
    ├── dags/                   # DAG definitions
    │   ├── daily_pipeline.py
    │   └── backfill_pipeline.py
    ├── config/
    │   └── airflow.cfg
    ├── logs/                   # Task execution logs
    └── plugins/
```


## Local Setup

### Prerequisites
- Docker and Docker Compose installed
- Python 3.10+
- MotherDuck account
- Deye Cloud API credentials

### Setup
1. Create the environment file
```
cp .env.example .env
# Edit .env with your credentials
```

2. Start Airflow
```
docker-compose up airflow-init
docker-compose up -d
```

3. Open the Airflow UI
```
URL: http://localhost:8080
Username: (from _AIRFLOW_WWW_USER_USERNAME in .env)
Password: (from _AIRFLOW_WWW_USER_PASSWORD in .env)
```

### Local Development
#### Local dbt Development
`profiles.yml` defaults to `prod` (MotherDuck), so use `--target dev` for local work:

```
# Run models locally
uv run dbt run --project-dir transform --target dev

# Run tests
uv run dbt test --project-dir transform --target dev

# Generate documentation
uv run dbt docs generate --project-dir transform --target dev
uv run dbt docs serve --project-dir transform --target dev
```

#### Running Jobs Locally (Without Airflow)
```
# Install uv first
pip install uv

# Sync all dependencies
uv sync

# Solar job
uv run python -m ingest.jobs.daily_solar_job

# Weather job
uv run python -m ingest.jobs.daily_weather_job

# Backfills
uv run python -m ingest.jobs.backfill_solar_job --start-date YYYY-MM-DD --end-date YYYY-MM-DD
uv run python -m ingest.jobs.backfill_weather_job --start-date YYYY-MM-DD --end-date YYYY-MM-DD
```
