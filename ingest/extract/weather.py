import pandas as pd
import logging
from ingest.client.openmeteo_api import OpenMeteoClient

logger = logging.getLogger(__name__)

class WeatherExtractor:
    def __init__(self):
        self.client = OpenMeteoClient()
    
    # weather data is inclusive of both start date and end date
    def extract(self, start_date: str, end_date: str) -> pd.DataFrame:
        try:
            response = self.client.get_weather_data(
                start_date=start_date, 
                end_date=end_date
            )
            
            hourly_df = self._transform_hourly(response)
            daily_df = self._transform_daily(response)

            return hourly_df, daily_df
        except Exception as err:
            logger.error(f"failed to extract weather data: {str(err)}")
            raise
    
    def _transform_hourly(self, response: dict) -> pd.DataFrame:
        hourly = response.Hourly()
        hourly_relative_humidity_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_wind_speed_10m = hourly.Variables(1).ValuesAsNumpy()
        hourly_is_day = hourly.Variables(2).ValuesAsNumpy()
        hourly_sunshine_duration = hourly.Variables(3).ValuesAsNumpy()
        hourly_temperature_2m = hourly.Variables(4).ValuesAsNumpy()
        hourly_cloud_cover = hourly.Variables(5).ValuesAsNumpy()
        hourly_rain = hourly.Variables(6).ValuesAsNumpy()
        hourly_weather_code = hourly.Variables(7).ValuesAsNumpy()

        hourly_data = {"timestamp": pd.date_range(
            start = pd.to_datetime(hourly.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
            end =  pd.to_datetime(hourly.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}

        hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
        hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
        hourly_data["is_day"] = hourly_is_day
        hourly_data["sunshine_duration"] = hourly_sunshine_duration
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["cloud_cover"] = hourly_cloud_cover
        hourly_data["rain"] = hourly_rain
        hourly_data["weather_code"] = hourly_weather_code

        return pd.DataFrame(data=hourly_data)
    
    def _transform_daily(self, response: dict) -> pd.DataFrame:
        daily = response.Daily()
        daily_shortwave_radiation_sum = daily.Variables(0).ValuesAsNumpy()
        daily_sunshine_duration = daily.Variables(1).ValuesAsNumpy()
        daily_daylight_duration = daily.Variables(2).ValuesAsNumpy()
        daily_cloud_cover_mean = daily.Variables(3).ValuesAsNumpy()
        daily_temperature_2m_mean = daily.Variables(4).ValuesAsNumpy()
        daily_relative_humidity_2m_mean = daily.Variables(5).ValuesAsNumpy()
        daily_rain_sum = daily.Variables(6).ValuesAsNumpy()
        daily_wind_speed_10m_mean = daily.Variables(7).ValuesAsNumpy()
        daily_weather_code = daily.Variables(8).ValuesAsNumpy()

        daily_data = {"timestamp": pd.date_range(
            start = pd.to_datetime(daily.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
            end =  pd.to_datetime(daily.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily.Interval()),
            inclusive = "left"
        )}

        daily_data["shortwave_radiation_sum"] = daily_shortwave_radiation_sum
        daily_data["sunshine_duration"] = daily_sunshine_duration
        daily_data["daylight_duration"] = daily_daylight_duration
        daily_data["cloud_cover_mean"] = daily_cloud_cover_mean
        daily_data["temperature_2m_mean"] = daily_temperature_2m_mean
        daily_data["relative_humidity_2m_mean"] = daily_relative_humidity_2m_mean
        daily_data["rain_sum"] = daily_rain_sum
        daily_data["wind_speed_10m_mean"] = daily_wind_speed_10m_mean
        daily_data["weather_code"] = daily_weather_code

        return pd.DataFrame(data=daily_data)