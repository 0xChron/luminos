import pandas as pd
import logging
from ingest.client.deye_api import DeyeCloudClient
from ingest.config import Config

logger = logging.getLogger(__name__)

class SolarExtractor:
    def __init__(self):
        self.client = DeyeCloudClient()

    def extract(self, start_timestamp: int, end_timestamp: int) -> pd.DataFrame:
        try:
            raw_data = self.client.get_solar_data(
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
            )
            
            return self._transform(raw_data)
        except Exception as err:
            logger.error(f"failed to extract solar data: {str(err)}")
            raise
    
    def _transform(self, raw_data: dict) -> pd.DataFrame:
        records = raw_data['stationDataItems']

        df = pd.DataFrame(records)
        df = df.rename(columns={
            'timeStamp': 'timestamp',
            'generationPower': 'generation',
            'consumptionPower': 'consumption',
            'gridPower': 'grid_feed_in',
            'purchasePower': 'grid_purchase',
            'chargePower': 'charge_power',
            'dischargePower': 'discharge_power',
            'batterySOC': 'battery_soc'
        })

        df = df[['timestamp', 'generation', 'consumption', 'grid_feed_in', 
            'grid_purchase', 'charge_power', 'discharge_power', 'battery_soc']]
        return df
    

