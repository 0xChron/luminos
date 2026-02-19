import requests
import hashlib
from ingest.config import Config


class DeyeCloudClient:
    def __init__(self):
        self.token_url = Config.DEYE_BASE_URL + '/account/token?appId=' + Config.APP_ID
        self.solar_data_url = Config.DEYE_BASE_URL + '/station/history/power'
        self.app_id = Config.APP_ID
        self.app_secret = Config.APP_SECRET
        self.email = Config.EMAIL
        self.password = Config.PASSWORD
        self.station_id = Config.STATION_ID
        self.token = None


    def get_token(self) -> str:
        sha256_hash = hashlib.sha256()
        sha256_hash.update(self.password.encode('utf-8'))
        password_hash = sha256_hash.hexdigest()
        headers = {'Content-Type': 'application/json'}

        data = {
            'appSecret': self.app_secret,
            'email': self.email,
            'password': password_hash
        }

        try:
            response = requests.post(self.token_url, headers=headers, json=data)
            response.raise_for_status()
            self.token = response.json().get('accessToken')
            return self.token
        
        except requests.exceptions.HTTPError as err:
            print(f'HTTP error occurred: {err}')
        except Exception as err:
            print(f'Other error occurred: {err}')


    def get_solar_data(self, start_timestamp: int, end_timestamp: int) -> dict:
        data = {
            "endTimestamp": end_timestamp,
            "startTimestamp": start_timestamp,
            "stationId": self.station_id
        }

        try:
            response = requests.post(self.solar_data_url, headers=self._get_headers(), json=data)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as err:
            print(f'HTTP error occurred: {err}')
        except Exception as err:
            print(f'Other error occurred: {err}')


    def _get_headers(self) -> dict[str, str]:
        if not self.token:
            self.get_token()
        return {'Content-Type': 'application/json', 'Authorization': 'bearer ' + self.token}