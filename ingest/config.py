import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # deye api config
    EMAIL = os.getenv('EMAIL')
    PASSWORD = os.getenv('PASSWORD')
    APP_ID = os.getenv('APP_ID')
    APP_SECRET = os.getenv('APP_SECRET')
    DEVICE_SN = os.getenv('DEVICE_SN')
    STATION_ID = os.getenv('STATION_ID')
    DEYE_BASE_URL = 'https://eu1-developer.deyecloud.com/v1.0'

    # openmeteo weather api config
    LATITUDE = os.getenv('LATITUDE')
    LONGITUDE = os.getenv('LONGITUDE')
    TIMEZONE = os.getenv('TIMEZONE', 'Asia/Singapore')
    WEATHER_BASE_URL = 'https://api.open-meteo.com/v1/forecast'

    DUCKDB_PATH = 'weather_warehouse.duckdb'

    SOLAR_LAG_DAYS = 1
    WEATHER_LOOKBACK_DAYS = 7