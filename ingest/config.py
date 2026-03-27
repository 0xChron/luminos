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
    WEATHER_BASE_URL = 'https://archive-api.open-meteo.com/v1/archive'
    TIMEZONE = "Asia/Singapore"
    HOURLY_PARAMETERS = [
        "relative_humidity_2m", 
        "wind_speed_10m", 
        "is_day", 
        "sunshine_duration", 
        "temperature_2m", 
        "cloud_cover", 
        "rain", 
        "weather_code"
        ]
    DAILY_PARAMETERS = [
        "shortwave_radiation_sum", 
        "sunshine_duration", 
        "daylight_duration", 
        "cloud_cover_mean", 
        "temperature_2m_mean", 
        "relative_humidity_2m_mean", 
        "rain_sum", 
        "wind_speed_10m_mean", 
        "weather_code"
        ]


    DEV_DUCKDB_PATH = os.getenv('DUCKDB_PATH')
    PROD_DUCKDB_PATH = os.getenv('PROD_DUCKDB_PATH')

    SOLAR_LAG_DAYS = 1
    WEATHER_LOOKBACK_DAYS = 7