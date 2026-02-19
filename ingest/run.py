# from ingest.client.openmeteo_api import OpenMeteoClient
from ingest.config import Config
from ingest.extract.solar import SolarExtractor
from ingest.extract.weather import WeatherExtractor
from datetime import datetime, timezone

def test_solar_extract():
    timestamp = datetime.now(timezone.utc).timestamp()
    print(timestamp)
    solar_extractor = SolarExtractor()

    yesterday = timestamp - 86400
    solar_data = solar_extractor.extract(yesterday)
    print(solar_data)

def test_weather_extract():
    weather_extractor = WeatherExtractor(start_date="2026-02-03", end_date="2026-02-15")
    hourly_df, daily_df = weather_extractor.extract()

    print(hourly_df.head())
    print(daily_df.head())


if __name__ == "__main__":
    # test_solar_extract()
    test_weather_extract()