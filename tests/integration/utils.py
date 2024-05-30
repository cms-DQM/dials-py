import os

from cmsdials import Dials
from cmsdials.auth.secret_key import Credentials


def setup_dials_object() -> Dials:
    secret_key = os.getenv("SECRET_KEY")
    base_url = os.getenv("BASE_URL")
    creds = Credentials(token=secret_key)
    return Dials(creds, base_url=base_url)
