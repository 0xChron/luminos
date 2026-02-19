import openmeteo_requests
import requests_cache
from retry_requests import retry
from ingest.config import Config

class OpenMeteoClient:
    def __init__(self, 
            latitude: float = Config.LATITUDE, 
            longitude: float = Config.LONGITUDE, 
            timezone: str = Config.TIMEZONE
        ):
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.url = Config.WEATHER_BASE_URL
        self.hourly_parameters = ["temperature_2m", 
            "cloud_cover", 
            "precipitation", 
            "wind_speed_10m", 
            "relative_humidity_2m", 
            "weather_code"
        ]
        self.daily_parameters = ["shortwave_radiation_sum", 
            "sunshine_duration", 
            "daylight_duration", 
            "uv_index_clear_sky_max", 
            "temperature_2m_max", 
            "temperature_2m_min"
        ]
        self.client = self._initialize_client()


    def get_weather_data(self) -> dict:
        data = {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'hourly': self.hourly_parameters,
            'daily': self.daily_parameters,
            'timezone': self.timezone
        }

        try:
            response = self.client.weather_api(self.url, params=data)
            return response[0]

        except Exception as err:
            print(f"Error fetching weather data: {err}")
            return None
        
    def _initialize_client(self):
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        return openmeteo_requests.Client(session=retry_session)