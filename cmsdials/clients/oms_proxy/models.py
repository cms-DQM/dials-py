from typing import Literal, Union

from pydantic import BaseModel


class OMSFilter(BaseModel):
    attribute_name: str
    value: Union[str, int, float]
    operator: Literal["EQ", "NEQ", "LT", "GT", "LE", "GE", "LIKE"]


class OMSPage(BaseModel):
    attribute_name: str
    value: int
