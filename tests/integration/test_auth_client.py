import os
from datetime import datetime, timedelta
from typing import Union

import pytest
from requests.exceptions import HTTPError

from cmsdials import Dials
from cmsdials.auth.bearer import Credentials as BearerCredentials
from cmsdials.auth.client import AuthClient
from cmsdials.auth.models import Token
from cmsdials.auth.secret_key import Credentials as SecretKeyCredentials
from cmsdials.clients.h1d.models import LumisectionHistogram1D


BASE_URL = os.getenv("BASE_URL")


def __setup_dials_from_creds_and_test(creds: Union[SecretKeyCredentials, BearerCredentials]) -> None:
    dials = Dials(creds, base_url=BASE_URL)
    data = dials.h1d.get(dataset_id=14677060, run_number=367112, ls_number=10, me_id=1)
    assert isinstance(data, LumisectionHistogram1D)


def test_secret_key_success() -> None:
    secret_key = os.getenv("SECRET_KEY")
    creds = SecretKeyCredentials(token=secret_key)
    __setup_dials_from_creds_and_test(creds)


def test_secret_key_fail() -> None:
    creds = SecretKeyCredentials(token="123456789")
    with pytest.raises(HTTPError, match=r"403 Client Error: Forbidden for url"):
        __setup_dials_from_creds_and_test(creds)


# This cannot be tested automatically since the `device_auth_flow` prints to stdout the url
# the user needs to access in order to authenticate and pytest only enable "live log call"
# if you specify the parameter "--log-cli-level=INFO".
# def test_bearer_success() -> None:
#     from cmsdials.auth.client import AuthClient
#     auth = AuthClient()
#     token = auth.device_auth_flow()
#     creds = BearerCredentials.from_authclient_token(token)
#     __setup_dials_from_creds_and_test(creds)


def test_bearer_fail() -> None:
    token = Token(
        access_token="123456789",
        expires_in=600,
        refresh_expires_in=12000,
        refresh_token="123456789",
        token_type="Bearer",
        expires_at=datetime.now() + timedelta(seconds=600),
        refresh_expires_at=datetime.now() + timedelta(seconds=12000),
    )
    auth = AuthClient(base_url=BASE_URL)
    creds = BearerCredentials.from_authclient_token(token, client=auth)
    with pytest.raises(HTTPError, match=r"403 Client Error: Forbidden for url"):
        __setup_dials_from_creds_and_test(creds)
