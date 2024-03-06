from typing import Optional

from .auth._base import BaseCredentials
from .clients.bad_file_index.client import BadFileIndexClient
from .clients.file_index.client import FileIndexClient
from .clients.h1d.client import LumisectionHistogram1DClient
from .clients.h2d.client import LumisectionHistogram2DClient
from .clients.lumisection.client import LumisectionClient
from .clients.run.client import RunClient


class Dials:
    def __init__(self, creds: BaseCredentials, nthreads: Optional[int] = None) -> None:
        self.bad_file_index = BadFileIndexClient(creds, nthreads=nthreads)
        self.file_index = FileIndexClient(creds, nthreads=nthreads)
        self.h1d = LumisectionHistogram1DClient(creds, nthreads=nthreads)
        self.h2d = LumisectionHistogram2DClient(creds, nthreads=nthreads)
        self.lumi = LumisectionClient(creds, nthreads=nthreads)
        self.run = RunClient(creds, nthreads=nthreads)
