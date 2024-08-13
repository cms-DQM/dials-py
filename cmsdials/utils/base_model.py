from importlib import util as importlib_util
from typing import Optional

from pydantic import BaseModel, Field


if importlib_util.find_spec("pandas"):
    import pandas as pd

    PANDAS_NOT_INSTALLED = False
else:
    PANDAS_NOT_INSTALLED = True


class OBaseModel(BaseModel):
    def cleandict(self):
        return {key: value for key, value in self.dict().items() if value is not None}


class PaginatedBaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    exception: Optional[BaseException] = Field(default=None)

    def to_pandas(self):
        if PANDAS_NOT_INSTALLED:
            raise RuntimeError(
                "The 'pandas' package is not installed, you can re-install cmsdials specifying the pandas extra: pip install cmsdials[pandas]"
            )
        return pd.DataFrame([res.__dict__ for res in self.results])
