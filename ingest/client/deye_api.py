import hashlib
import logging
import time

import requests
from ingest.config import Config

logger = logging.getLogger(__name__)

# (connect timeout, read timeout) seconds
REQUEST_TIMEOUT = (5, 30)
MAX_ATTEMPTS = 3
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
SUCCESS_CODE = "1000000"


class DeyeAPIError(Exception):
    """Raised when Deye returns HTTP OK but a failed business response."""

    def __init__(self, message: str, *, code: str | None = None, payload: dict | None = None):
        super().__init__(message)
        self.code = code
        self.payload = payload or {}


class DeyeCloudClient:
    def __init__(self):
        self.token_url = Config.DEYE_BASE_URL + "/account/token?appId=" + Config.APP_ID
        self.solar_data_url = Config.DEYE_BASE_URL + "/station/history/power"
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
        sha256_hash.update(self.password.encode("utf-8"))
        password_hash = sha256_hash.hexdigest()

        data = {
            "appSecret": self.app_secret,
            "email": self.email,
            "password": password_hash,
        }

        try:
            token_data = self._post_json(
                self.token_url,
                headers={"Content-Type": "application/json"},
                json_body=data,
            )

            access_token = token_data.get("accessToken")
            expires_in = token_data.get("expiresIn")
            if not access_token or expires_in is None:
                raise DeyeAPIError(
                    "Deye token response missing accessToken or expiresIn",
                    code=token_data.get("code"),
                    payload=token_data,
                )

            self.token = access_token
            self.refresh_token = token_data.get("refreshToken")
            self.token_expiry = int(time.time()) + int(expires_in)
            return self.token

        except (requests.exceptions.RequestException, DeyeAPIError) as err:
            logger.error(f"failed to obtain Deye token: {err}")
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
            "stationId": self.station_id,
        }

        try:
            payload = self._post_json(
                self.solar_data_url,
                headers=self._get_headers(),
                json_body=data,
                refresh_auth_on_failure=True,
            )
            logger.info(
                f"successfully fetched solar data for timestamps {start_timestamp} to {end_timestamp}"
            )
            return payload

        except (requests.exceptions.RequestException, DeyeAPIError) as err:
            logger.error(f"failed to fetch Deye solar data: {err}")
            raise

    def _get_headers(self) -> dict[str, str]:
        if self._is_token_expired():
            self.get_token()

        if not self.token:
            raise DeyeAPIError("No Deye access token available")

        return {
            "Content-Type": "application/json",
            "Authorization": "bearer " + self.token,
        }

    def _post_json(
        self,
        url: str,
        *,
        headers: dict[str, str],
        json_body: dict,
        refresh_auth_on_failure: bool = False,
    ) -> dict:
        """POST with timeouts, retry on 429/5xx, and validate Deye business success."""
        auth_refreshed = False
        attempt = 0

        while attempt < MAX_ATTEMPTS:
            attempt += 1
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json=json_body,
                    timeout=REQUEST_TIMEOUT,
                )
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
                if attempt >= MAX_ATTEMPTS:
                    raise
                self._backoff(attempt)
                logger.warning(f"Deye request failed ({err}); retry {attempt}/{MAX_ATTEMPTS}")
                continue

            if response.status_code in RETRYABLE_STATUS_CODES and attempt < MAX_ATTEMPTS:
                self._backoff(attempt)
                logger.warning(
                    f"Deye returned HTTP {response.status_code}; retry {attempt}/{MAX_ATTEMPTS}"
                )
                continue

            # HTTP 401: force token refresh once, then retry
            if (
                response.status_code == 401
                and refresh_auth_on_failure
                and not auth_refreshed
            ):
                logger.info("Deye returned HTTP 401; refreshing token and retrying once")
                self._invalidate_token()
                headers = self._get_headers()
                auth_refreshed = True
                attempt -= 1  # auth refresh retry does not consume a transient attempt
                continue

            response.raise_for_status()
            payload = response.json()

            if self._is_business_success(payload):
                return payload

            # Deye often returns HTTP 200 with success=false for bad/expired tokens
            if (
                refresh_auth_on_failure
                and not auth_refreshed
                and self._is_auth_failure(payload)
            ):
                logger.info(
                    "Deye business auth failure (%s); refreshing token and retrying once",
                    payload.get("msg"),
                )
                self._invalidate_token()
                headers = self._get_headers()
                auth_refreshed = True
                attempt -= 1
                continue

            raise DeyeAPIError(
                f"Deye API error code={payload.get('code')} msg={payload.get('msg')}",
                code=payload.get("code"),
                payload=payload,
            )

        raise DeyeAPIError("Deye request exhausted retries without a response")

    @staticmethod
    def _is_business_success(payload: dict) -> bool:
        if payload.get("success") is True:
            return True
        return str(payload.get("code")) == SUCCESS_CODE

    @staticmethod
    def _is_auth_failure(payload: dict) -> bool:
        msg = str(payload.get("msg") or "").lower()
        code = str(payload.get("code") or "")
        auth_markers = ("auth", "token", "unauthorized", "login", "permission")
        return any(marker in msg for marker in auth_markers) or code in {
            "401",
            "1000001",
            "1000002",
        }

    def _invalidate_token(self) -> None:
        self.token = None
        self.refresh_token = None
        self.token_expiry = None

    @staticmethod
    def _backoff(attempt: int) -> None:
        time.sleep(min(2 ** (attempt - 1), 4))
