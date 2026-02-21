from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from ingest.extract.solar import SolarExtractor
from ingest.load.duckdb_loader import DuckDBLoader
from ingest.config import Config
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(module)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def run_solar_job(target_timestamp=None):
    tz = ZoneInfo(Config.TIMEZONE)

    if target_timestamp is None:
        today = datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - timedelta(days=1)
        logger.info(f"date window: {yesterday} -> {today}")

        # unix timestamp: always get yesterday's solar data, as today's data may not be complete
        start_timestamp = int(yesterday.timestamp())
        end_timestamp = int(today.timestamp()) - 1 # to exclude 00:00 data point of the next day

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