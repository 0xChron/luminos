from dagster import Definitions
from .assets.ingest_assets import raw_solar_data, raw_weather_data
from .assets.dbt_assets import luminos_dbt_assets
from .jobs import daily_pipeline_job, ingestion_only_job, dbt_only_job
from .schedules import daily_schedule
from .resources import dbt_resource

defs = Definitions(
    assets=[raw_solar_data, raw_weather_data, luminos_dbt_assets],
    jobs=[daily_pipeline_job, ingestion_only_job, dbt_only_job],
    schedules=[daily_schedule],
    resources={"dbt": dbt_resource}
)