from datetime import datetime

from pydantic import BaseModel


class Device(BaseModel):
    device_code: str
    verification_uri_complete: str
    expires_in: int


class DeviceToken(BaseModel):
    access_token: str
    expires_in: int
    refresh_expires_in: int
    refresh_token: str
    token_type: str


RefreshToken = DeviceToken


class Token(DeviceToken):
    expires_at: datetime
    refresh_expires_at: datetime
