from typing import Optional

from .auth._base import BaseCredentials
from .clients.file_index.client import FileIndexClient
from .clients.h1d.client import LumisectionHistogram1DClient
from .clients.h2d.client import LumisectionHistogram2DClient
from .clients.lumisection.client import LumisectionClient
from .clients.mes.client import MonitoringElementClient
from .clients.run.client import RunClient


class Dials:
    def __init__(self, creds: BaseCredentials, workspace: Optional[str] = None, *args, **kwargs) -> None:
        self.file_index = FileIndexClient(creds, workspace, *args, **kwargs)
        self.h1d = LumisectionHistogram1DClient(creds, workspace, *args, **kwargs)
        self.h2d = LumisectionHistogram2DClient(creds, workspace, *args, **kwargs)
        self.lumi = LumisectionClient(creds, workspace, *args, **kwargs)
        self.run = RunClient(creds, workspace, *args, **kwargs)
        self.mes = MonitoringElementClient(creds, workspace, *args, **kwargs)
