import os
from typing import Optional

from cmsdials import Dials
from cmsdials.auth.secret_key import Credentials


DEFAULT_TEST_WORKSPACE = "tracker"


def setup_dials_object(workspace: Optional[str] = None) -> Dials:
    secret_key = os.getenv("SECRET_KEY")
    base_url = os.getenv("BASE_URL")
    creds = Credentials(token=secret_key)
    return Dials(creds, base_url=base_url, workspace=workspace)
