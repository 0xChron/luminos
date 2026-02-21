import requests
import hashlib
import time
import logging
from ingest.config import Config

logger = logging.getLogger(__name__)

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
        self.refresh_token = None
        self.token_expiry = None 


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

            token_data = response.json()
            self.token = token_data.get('accessToken')
            self.refresh_token = token_data.get('refreshToken')

            expires_in = int(token_data.get('expiresIn'))
            self.token_expiry = int(time.time()) + expires_in

            return self.token
        
        except requests.exceptions.HTTPError as err:
            logger.error(f'http error occurred: {err}')
            raise
        except Exception as err:
            logger.error(f'other error occurred: {err}')
            raise

    def _is_token_expired(self) -> bool:
        if not self.token or not self.token_expiry:
            return True
    
        # refresh 5 minutes before actual expiry
        current_time = int(time.time())
        buffer_seconds = 300
        
        return current_time >= (self.token_expiry - buffer_seconds)


    def get_solar_data(self, start_timestamp: int, end_timestamp: int) -> dict:
        data = {
            "endTimestamp": end_timestamp,
            "startTimestamp": start_timestamp,
            "stationId": self.station_id
        }

        try:
            response = requests.post(self.solar_data_url, headers=self._get_headers(), json=data)
            response.raise_for_status()

            logger.info(f"successfully fetched solar data for timestamps {start_timestamp} to {end_timestamp}")
            return response.json()
        
        except requests.exceptions.HTTPError as err:
            # if 401 unauthorized, force token refresh and retry once
            if err.response.status_code == 401:
                logger.info("Token expired, refreshing...")
                self.token = None
                self.token_expiry = None
                response = requests.post(self.solar_data_url, headers=self._get_headers(), json=data)
                response.raise_for_status()
                return response.json()
            logger.error(f'http error occurred: {err}')
            raise
        except Exception as err:
            logger.error(f'other error occurred: {err}')
            raise   


    def _get_headers(self) -> dict[str, str]:
        if self._is_token_expired():
            self.get_token()

        return {'Content-Type': 'application/json', 'Authorization': 'bearer ' + self.token}