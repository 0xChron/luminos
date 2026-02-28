import openmeteo_requests
import requests_cache
import logging
from retry_requests import retry
from ingest.config import Config

logger = logging.getLogger(__name__)

class OpenMeteoClient:
    def __init__(self, 
            latitude: float = Config.LATITUDE, 
            longitude: float = Config.LONGITUDE, 
            timezone: str = Config.TIMEZONE,
        ):
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.url = Config.WEATHER_BASE_URL
        self.hourly_parameters = Config.HOURLY_PARAMETERS
        self.daily_parameters = Config.DAILY_PARAMETERS

        self.client = self._initialize_client()
        


    def get_weather_data(self, start_date: str, end_date: str) -> dict:
        data = {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'hourly': self.hourly_parameters,
            'daily': self.daily_parameters,
            'timezone': self.timezone,
        	"start_date": start_date,
	        "end_date": end_date,
        }

        try:
            response = self.client.weather_api(self.url, params=data)

            logger.info(f"successfully fetched weather data for date range {start_date} to {end_date}")
            return response[0]

        except Exception as err:
            logger.error(f"error fetching weather data: {err}")
            raise
        
    def _initialize_client(self):
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        return openmeteo_requests.Client(session=retry_session)