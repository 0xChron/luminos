import logging
import argparse
from datetime import datetime
from zoneinfo import ZoneInfo
from ingest.extract.solar import SolarExtractor
from ingest.load.duckdb_loader import DuckDBLoader
from ingest.config import Config
from ingest.utils.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def run_backfill_solar_job(start_date: str, end_date: str) -> None:
    tz = ZoneInfo(Config.TIMEZONE)

    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=tz).timestamp())
    end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=tz).timestamp()) - 1 # to exclude 00:00 data point of the next day
    logger.info(f"date window: {start_date} -> {end_date}")

    try:
        extractor = SolarExtractor()
        solar_df = extractor.extract(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp
        )
        logger.info(f"extracted {len(solar_df)} solar records to backfill")

        with DuckDBLoader() as loader:
            records_count = loader.load_solar_data(solar_df)
            logger.info(f"loaded {records_count} solar records to DuckDB")
        
        logger.info("solar data backfill completed successfully")
    
    except Exception as err:
        logger.error(f"solar data pull failed: {str(err)}")
        raise
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="backfill solar energy data")
    parser.add_argument("--start-date", required=True, help="start date in YYYY-MM-DD format")
    parser.add_argument("--end-date", required=True, help="end date in YYYY-MM-DD format")
    args = parser.parse_args()
    
    run_backfill_solar_job(start_date=args.start_date, end_date=args.end_date)


