from ingest.extract.weather import WeatherExtractor
from ingest.load.duckdb_loader import DuckDBLoader
import logging
import argparse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(module)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def run_backfill_weather_job(start_date: str, end_date: str) -> None:
    try:
        extractor = WeatherExtractor()
        hourly_df, daily_df = extractor.extract(
            start_date=start_date,
            end_date=end_date
        )
        logger.info(f"extracted {len(hourly_df)} hourly, {len(daily_df)} daily weather records")

        with DuckDBLoader() as loader:
            hourly_loaded = loader.load_weather_hourly(hourly_df)
            daily_loaded = loader.load_weather_daily(daily_df)
            logger.info(f"loaded {hourly_loaded} hourly, {daily_loaded} daily records to DuckDB")

        logger.info("weather data backfill completed successfully")
    except Exception as err:
        logger.error(f"weather data backfill failed: {str(err)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="backfill solar energy data")
    parser.add_argument("--start-date", required=True, help="start date in YYYY-MM-DD format")
    parser.add_argument("--end-date", required=True, help="end date in YYYY-MM-DD format")
    args = parser.parse_args()

    run_backfill_weather_job(start_date=args.start_date, end_date=args.end_date)