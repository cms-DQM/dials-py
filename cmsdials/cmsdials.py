from typing import Optional

from .auth._base import BaseCredentials
from .clients.dataset_index.client import DatasetIndexClient
from .clients.file_index.client import FileIndexClient
from .clients.h1d.client import LumisectionHistogram1DClient
from .clients.h2d.client import LumisectionHistogram2DClient
from .clients.lumisection.client import LumisectionClient
from .clients.mes.client import MonitoringElementClient
from .clients.ml_bad_lumisection.client import MLBadLumisectionClient
from .clients.ml_models_index.client import MLModelsIndexClient
from .clients.oms_proxy.client import OMSProxyClient
from .clients.run.client import RunClient


class Dials:
    def __init__(self, creds: BaseCredentials, workspace: Optional[str] = None, *args, **kwargs) -> None:
        self.dataset_index = DatasetIndexClient(creds, workspace, *args, **kwargs)
        self.file_index = FileIndexClient(creds, workspace, *args, **kwargs)
        self.h1d = LumisectionHistogram1DClient(creds, workspace, *args, **kwargs)
        self.h2d = LumisectionHistogram2DClient(creds, workspace, *args, **kwargs)
        self.lumi = LumisectionClient(creds, workspace, *args, **kwargs)
        self.run = RunClient(creds, workspace, *args, **kwargs)
        self.mes = MonitoringElementClient(creds, workspace, *args, **kwargs)
        self.oms = OMSProxyClient(creds, *args, **kwargs)
        self.ml_bad_lumis = MLBadLumisectionClient(creds, workspace, *args, **kwargs)
        self.ml_models_index = MLModelsIndexClient(creds, workspace, *args, **kwargs)
