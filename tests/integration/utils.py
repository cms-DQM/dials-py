import os

from cmsdials import Dials
from cmsdials.auth.secret_key import Credentials


def setup_dials_object() -> Dials:
    secret_key = os.getenv("SECRET_KEY")
    creds = Credentials(token=secret_key)
    return Dials(creds)
