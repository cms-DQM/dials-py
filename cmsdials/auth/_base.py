import threading
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum
from typing import Mapping

from .exceptions import ImpossibleToRefreshToken


class TokenState(Enum):
    """
    Tracks the state of a token.

    FRESH: The token is valid and can be used.
    STALE: The token is close to expired, it can be used but you also should trigger a non blocking refresh.
    EXPIRED: The token is expired but the refresh token is valid. You must trigger a block refresh.
    INVALID: Both the token and refresh token are expired.
    """

    FRESH = 1
    STALE = 2
    EXPIRED = 3
    INVALID = 4


class BaseCredentials(ABC):
    """
    Base class for all credentials.
    """

    def __init__(self):
        self.token = None
        self.expires_at = None
        self.expires_in = None
        self.refresh_expires_at = None
        self.refresh_expires_in = None
        self.refresh_token = None
        self.token_type = None
        self._stale_lock = threading.Lock()
        self._expired_lock = threading.Lock()

    @property
    def stale(self) -> bool:
        """
        States if token is staled.
        """
        if not self.expires_at:
            return False
        return self.expires_at > datetime.now() > (self.expires_at - timedelta(seconds=0.1 * self.expires_in))

    @property
    def expired(self) -> bool:
        """
        States if token is expired.
        """
        if not self.expires_at:
            return False
        return datetime.now() >= self.expires_at

    @property
    def refresh_expired(self) -> bool:
        """
        States if refresh token is expired.
        """
        if not self.refresh_expires_at:
            return False
        return datetime.now() >= self.refresh_expires_at

    @property
    def token_state(self):
        """
        See `:obj:`TokenState`
        """
        # Credentials that can't expire are always treated as fresh.
        if self.expires_at is None:
            return TokenState.FRESH

        if self.stale:
            return TokenState.STALE

        if self.expired and not self.refresh_expired:
            return TokenState.EXPIRED

        if self.expired and self.refresh_expired:
            return TokenState.INVALID

        return TokenState.FRESH

    @abstractmethod
    def apply(self, headers: Mapping[str, str]) -> None:
        """
        Apply the token to the authentication header.
        """
        raise NotImplementedError("apply must be implemented")

    @abstractmethod
    def refresh(self) -> None:
        """
        Performs credential-specific refresh logic.
        """
        raise NotImplementedError("refresh must be implemented")

    def _blocking_refresh(self) -> None:
        if self.token_state == TokenState.EXPIRED:
            self.refresh()

    def _nonblocking_refresh(self) -> None:
        self._stale_lock.acquire()
        self.refresh()
        self._stale_lock.release()

    def before_request(self, headers: Mapping[str, str]):
        """
        Performs credential-specific before request logic.
        """
        # If token is invalid (both token and refresh token expired): Throw error
        # User need to interactively authenticate again
        if self.token_state == TokenState.INVALID:
            raise ImpossibleToRefreshToken

        # If token is stale (token is close to expire)
        # Re-use the token but launch a new thread to refresh the token
        if self.token_state == TokenState.STALE and self._stale_lock.locked() is False:
            worker = threading.Thread(target=self._nonblocking_refresh)
            worker.start()

        # If token is expired (token is expired but refresh token is not expired)
        # Do not re-use the token, block the main thread and refresh before continuing
        # After refresh the token is fresh
        if self.token_state == TokenState.EXPIRED:
            self._expired_lock.acquire()
            self._blocking_refresh()
            self._expired_lock.release()

        # Put token in the header if token is fresh
        self.apply(headers)
