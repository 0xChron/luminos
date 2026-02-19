import pandas as pd
from ingest.client.deye_api import DeyeCloudClient

class SolarExtractor:
    def __init__(self):
        self.client = DeyeCloudClient()

    def extract(self, target_timestamp: int) -> pd.DataFrame:
        date_target = target_timestamp # fix
        date_before = target_timestamp - 86400 # fix 
        raw_data = self.client.get_solar_data(
            start_timestamp=date_before, 
            end_timestamp=date_target)
        
        return self._transform(raw_data)
    
    def _transform(self, raw_data: dict) -> pd.DataFrame:
        records = raw_data['stationDataItems']
        df = pd.DataFrame(records)
        df = df.rename(columns={
            'timeStamp': 'time_stamp',
            'generationPower': 'generation',
            'consumptionPower': 'consumption',
            'gridPower': 'grid_feed_in',
            'purchasePower': 'grid_purchase',
            'chargePower': 'charge_power',
            'dischargePower': 'discharge_power',
            'batterySOC': 'battery_soc'
        })

        df = df[['time_stamp', 'generation', 'consumption', 'grid_feed_in', 
            'grid_purchase', 'charge_power', 'discharge_power', 'battery_soc']]
        return df