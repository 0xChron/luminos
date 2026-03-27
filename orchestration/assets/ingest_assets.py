from dagster import asset, AssetExecutionContext, Output
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent


@asset(
    name="raw_solar_data",
    group_name="ingestion",
    description="extract solar energy data from deye api and load to duckdb raw layer",
    compute_kind="python"
)
def raw_solar_data(context: AssetExecutionContext) -> Output[bool]:
    context.log.info("starting solar data ingestion...")
    
    result = subprocess.run(
        ["uv", "run", "python", "-m", "ingest.jobs.daily_solar_job"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        context.log.info("solar ingestion succeeded")
        context.log.info(f"output: {result.stdout}")
        
        return Output(
            value=True,
            metadata={
                "status": "success",
                "records_processed": "Check logs for details",
                "stdout_preview": result.stdout[-500:] if result.stdout else "No output"
            }
        )
    else:
        context.log.error(f"solar ingestion failed with return code {result.returncode}")
        context.log.error(f"error output: {result.stderr}")
        raise Exception(f"solar ingestion failed: {result.stderr}")


@asset(
    name="raw_weather_data",
    group_name="ingestion",
    description="extract yesterday's weather data from open-meteo api and load to duckdb raw layer",
    compute_kind="python"
)
def raw_weather_data(context: AssetExecutionContext) -> Output[bool]:
    context.log.info("starting weather data ingestion...")
    
    result = subprocess.run(
        ["uv", "run", "python", "-m", "ingest.jobs.daily_weather_job"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        context.log.info("weather ingestion succeeded")
        context.log.info(f"output: {result.stdout}")
        
        return Output(
            value=True,
            metadata={
                "status": "success",
                "records_processed": "Check logs for details",
                "stdout_preview": result.stdout[-500:] if result.stdout else "No output"
            }
        )
    else:
        context.log.error(f"Weather ingestion failed with return code {result.returncode}")
        context.log.error(f"Error output: {result.stderr}")
        raise Exception(f"Weather ingestion failed: {result.stderr}")