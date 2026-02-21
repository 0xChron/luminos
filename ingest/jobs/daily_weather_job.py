from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from ingest.extract.weather import WeatherExtractor
from ingest.load.duckdb_loader import DuckDBLoader
from ingest.config import Config
from ingest.utils.logging import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

def run_weather_job(target_date=None):
    tz = ZoneInfo(Config.TIMEZONE)
    
    if target_date is None:
        # yyyy-mm-dd: always get yesterday's weather data, as today's data may not be complete
        target_date = (datetime.now(tz) - timedelta(days=1)).strftime("%Y-%m-%d")

    try:
        extractor = WeatherExtractor()
        hourly_df, daily_df = extractor.extract(
            start_date=target_date,
            end_date=target_date
        )

        logger.info(f"extracted {len(hourly_df)} hourly, {len(daily_df)} daily weather records")
        
        with DuckDBLoader() as loader:
            hourly_loaded = loader.load_weather_hourly(hourly_df)
            daily_loaded = loader.load_weather_daily(daily_df)
            logger.info(f"loaded {hourly_loaded} hourly, {daily_loaded} daily records to DuckDB")
        
        logger.info("weather data pull completed successfully")
        
    except Exception as err:
        logger.error(f"weather data pull failed: {str(err)}")
        raise

if __name__ == "__main__":
    run_weather_job()