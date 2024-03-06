import json
import os
import os.path
from datetime import datetime
from typing import Mapping, Optional

from ..utils._json import TokenDecoder, TokenEncoder
from ..utils.logger import logger
from ._base import BaseCredentials, TokenState
from .client import AuthClient
from .models import Token

DEFAULT_CACHE_DIR = ".cache"
DEFAULT_CACHE_FILENAME = "creds"


class Credentials(BaseCredentials):
    """
    Token credentials.
    These credential use a token to provide authorization to applications.
    """

    def __init__(
        self,
        token: str,
        expires_at: datetime,
        expires_in: int,
        refresh_expires_at: datetime,
        refresh_expires_in: int,
        refresh_token: str,
        token_type: str,
        cache_dir: str = DEFAULT_CACHE_DIR,
        client: Optional[AuthClient] = None,
    ):
        # Load parent class and overwrite token attributes
        super().__init__()
        self.token = token
        self.expires_at = expires_at
        self.expires_in = expires_in
        self.refresh_expires_at = refresh_expires_at
        self.refresh_expires_in = refresh_expires_in
        self.refresh_token = refresh_token
        self.token_type = token_type

        # Setup dir for caching credentials and authentication client
        self.cache_dir = cache_dir
        self.client = client or AuthClient()

        # If loaded token is expired, immediately refresh
        if self.token_state == TokenState.EXPIRED:
            self.refresh()

        # If loaded token is invalid, trigger authentication
        if self.token_state == TokenState.INVALID:
            logger.info("Access token and refresh token are expired, triggering device authentication flow...")
            token: Token = self.client.device_auth_flow()
            self._set_token(token)

        # Only cache if token is fresh
        if self.token_state == TokenState.FRESH:
            self.cache_credentials()

    @property
    def _token(self) -> Token:
        return Token(
            access_token=self.token,
            expires_in=self.expires_in,
            refresh_expires_in=self.refresh_expires_in,
            refresh_token=self.refresh_token,
            token_type=self.token_type,
            expires_at=self.expires_at,
            refresh_expires_at=self.refresh_expires_at,
        )

    @staticmethod
    def _handle_creds_filepath(cache_dir: str = DEFAULT_CACHE_DIR):
        cache_dir = cache_dir or DEFAULT_CACHE_DIR
        if os.path.isabs(cache_dir) is False:
            cache_dir = os.path.join(os.getcwd(), cache_dir)

        os.makedirs(cache_dir, exist_ok=True)
        return os.path.join(cache_dir, DEFAULT_CACHE_FILENAME)

    @staticmethod
    def from_authclient_token(
        token: Token, cache_dir: str = DEFAULT_CACHE_DIR, client: Optional[AuthClient] = None
    ) -> "Credentials":
        client = client or AuthClient()
        return Credentials(
            token=token.access_token,
            expires_in=token.expires_in,
            refresh_expires_in=token.refresh_expires_in,
            refresh_token=token.refresh_token,
            token_type=token.token_type,
            expires_at=token.expires_at,
            refresh_expires_at=token.refresh_expires_at,
            cache_dir=cache_dir,
            client=client,
        )

    @staticmethod
    def from_creds_file(cache_dir: str = DEFAULT_CACHE_DIR, client: Optional[AuthClient] = None) -> "Credentials":
        client = client or AuthClient()
        fpath = Credentials._handle_creds_filepath(cache_dir)
        try:
            with open(fpath, "r") as filebuffer:
                fcontents = json.load(filebuffer, cls=TokenDecoder)
            token = Token(**fcontents)
        except FileNotFoundError:
            logger.info("Credentials file not found, triggering device authentication flow...")
            token: Token = client.device_auth_flow()

        return Credentials.from_authclient_token(token, cache_dir, client)

    def _set_token(self, token: Token):
        self.token = token.access_token
        self.expires_at = token.expires_at
        self.expires_in = token.expires_in
        self.refresh_expires_at = token.refresh_expires_at
        self.refresh_expires_in = token.refresh_expires_in
        self.refresh_token = token.refresh_token
        self.token_type = token.token_type

    def cache_credentials(self) -> None:
        fpath = self._handle_creds_filepath(self.cache_dir)
        with open(fpath, "w") as filebuffer:
            json.dump(self._token.dict(), filebuffer, cls=TokenEncoder)

    def refresh(self) -> None:
        token: Token = self.client.refresh_token(self.token_type, self.token, self.refresh_token)
        self._set_token(token)
        self.cache_credentials()

    def apply(self, headers: Mapping[str, str]) -> None:
        """
        Apply the Client secret key token to the X-CLIENT-SECRET header.
        """
        headers["Authorization"] = f"{self.token_type} {self.token}"
