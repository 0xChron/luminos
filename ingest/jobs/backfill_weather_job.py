from ingest.extract.weather import WeatherExtractor
from ingest.load.duckdb_loader import DuckDBLoader
from datetime import timezone, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_backfill_weather_job(start_date: str, end_date: str) -> None:
    tz = timezone(timedelta(hours=8))

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
    START_DATE = "2026-02-02"
    END_DATE = "2026-02-19"
    run_backfill_weather_job(start_date=START_DATE, end_date=END_DATE)