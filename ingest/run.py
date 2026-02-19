from ingest.client.openmeteo_api import OpenMeteoClient
from ingest.config import Config


def main():
    openmeteo_client = OpenMeteoClient()
    weather_data = openmeteo_client.get_weather_data()
    print(weather_data)

if __name__ == "__main__":
    main()