from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from ingest.extract.solar import SolarExtractor
from ingest.load.duckdb_loader import DuckDBLoader
from ingest.config import Config
from ingest.utils.logging import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

def run_solar_job(target_timestamp=None):
    tz = ZoneInfo(Config.TIMEZONE)

    if target_timestamp is None:
        # always get yesterday's solar data, as today's data may not be complete
        day_start = datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    elif isinstance(target_timestamp, datetime):
        target_dt = target_timestamp if target_timestamp.tzinfo else target_timestamp.replace(tzinfo=tz)
        day_start = target_dt.astimezone(tz).replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        day_start = datetime.fromtimestamp(int(target_timestamp), tz=tz).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

    day_end = day_start + timedelta(days=1)
    start_timestamp = int(day_start.timestamp())
    end_timestamp = int(day_end.timestamp()) - 1  # exclude 00:00 of the next day
    logger.info(f"date window: {day_start} -> {day_end}")

    try:
        # unix timestamp format
        extractor = SolarExtractor()
        solar_df = extractor.extract(
            start_timestamp=start_timestamp, 
            end_timestamp=end_timestamp
        )
        logger.info(f"extracted {len(solar_df)} solar records")
        
        with DuckDBLoader() as loader:
            records_count = loader.load_solar_data(solar_df)
            logger.info(f"loaded {records_count} solar records to DuckDB")
        
        logger.info("solar data pull completed successfully")
        
    except Exception as err:
        logger.error(f"solar data pull failed: {str(err)}")
        raise

if __name__ == "__main__":
    run_solar_job()