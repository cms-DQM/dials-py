from collections.abc import Mapping

from ._base import BaseCredentials


class Credentials(BaseCredentials):
    """
    Client secret key credentials.
    These credential use Client secret key to provide authorization to applications.
    """

    def __init__(self, token: str) -> None:
        if not token:
            raise ValueError("token must be a non-empty Client secret key string")
        self.token = token

    @property
    def stale(self) -> bool:
        return False

    @property
    def expired(self) -> bool:
        return False

    @property
    def refresh_expired(self) -> bool:
        return False

    def refresh(self) -> None:
        return

    def apply(self, headers: Mapping[str, str]) -> None:
        """
        Apply the Client secret key token to the X-CLIENT-SECRET header.
        """
        headers["X-CLIENT-SECRET"] = self.token

    def before_request(self, headers: Mapping[str, str]):
        """
        Performs credential-specific before request logic.
        """
        self.apply(headers)
