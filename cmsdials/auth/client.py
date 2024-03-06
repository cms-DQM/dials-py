import time
from datetime import datetime, timedelta

import requests

from ..utils.api_client import BaseAPIClient
from ..utils.logger import logger
from .exceptions import PendingAuthorizationError
from .models import Device, DeviceToken, RefreshToken, Token


class AuthClient(BaseAPIClient):
    """
    Client for DIALS auth endpoint
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def new_device(self) -> Device:
        endpoint_url = self.api_url + "auth/new-device/"
        response = requests.get(
            url=endpoint_url,
            headers={
                "accept": "application/json",
            },
        )
        response.raise_for_status()
        response = response.json()
        return Device(**response)

    def device_token(self, device_code: str) -> Token:
        endpoint_url = self.api_url + "auth/device-token/"
        response = requests.post(
            url=endpoint_url,
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json={"device_code": device_code},
        )

        if response.status_code == 400 and "authorization_pending" in response.text:
            raise PendingAuthorizationError

        response.raise_for_status()
        response = response.json()
        curr_datetime = datetime.now()
        token = DeviceToken(**response)
        return Token(
            **token.dict(),
            expires_at=curr_datetime + timedelta(seconds=token.expires_in),
            refresh_expires_at=curr_datetime + timedelta(seconds=token.refresh_expires_in),
        )

    def refresh_token(self, token_type: str, access_token: str, refresh_token: str) -> Token:
        endpoint_url = self.api_url + "auth/refresh-token/"
        response = requests.post(
            url=endpoint_url,
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"{token_type} {access_token}",
            },
            json={"refresh_token": refresh_token},
        )
        response.raise_for_status()
        response = response.json()
        curr_datetime = datetime.now()
        token = RefreshToken(**response)
        return Token(
            **token.dict(),
            expires_at=curr_datetime + timedelta(seconds=token.expires_in),
            refresh_expires_at=curr_datetime + timedelta(seconds=token.refresh_expires_in),
        )

    def device_auth_flow(self):
        interval = 5  # seconds
        device = self.new_device()
        end_date = datetime.now() + timedelta(seconds=device.expires_in)

        logger.info(f"This device will expire in {device.expires_in} seconds.")
        logger.info(f"Go to the following url and authenticate: {device.verification_uri_complete}")
        logger.info(f"Checking authorization status every {interval} seconds...")

        while True:
            time.sleep(interval)
            curr_date = datetime.now()
            if curr_date > end_date:
                raise Exception("Action took too much time, device expired!")

            try:
                token = self.device_token(device_code=device.device_code)
                logger.info("Device authorized, authentication finished successfully!")
                return token
            except PendingAuthorizationError:
                logger.info("Device not authorized yet.")
