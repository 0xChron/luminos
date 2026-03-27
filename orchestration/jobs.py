from dagster import define_asset_job, AssetSelection

# main daily pipeline: ingestion + dbt transformations
daily_pipeline_job = define_asset_job(
    name="daily_pipeline",
    description="complete daily pipeline: ingest raw data → transform via dbt",
    selection=AssetSelection.all(),
)

ingestion_only_job = define_asset_job(
    name="ingestion_only",
    description="run only data ingestion jobs (solar + weather)",
    selection=AssetSelection.groups("ingestion"),
)

dbt_only_job = define_asset_job(
    name="dbt_only",
    description="run only dbt transformations (staging → marts → reports)",
    selection=AssetSelection.all() - AssetSelection.groups("ingestion"),  
)