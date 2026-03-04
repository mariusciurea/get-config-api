"""pydantic models for config"""

from typing import Annotated
from pydantic import BaseModel, Field, IPvAnyAddress, field_validator
from pydantic.error_wrappers import ValidationError


class NEConfigInput(BaseModel):
    id: int
    ne_name: Annotated[str, Field(min_length=3)]
    om_ip: str
    lte_ip: str
    enodeb_id: int


class NEConfigOutput(BaseModel):
    id: int
    ne_name: Annotated[str, Field(min_length=3)]
    om_ip: IPvAnyAddress
    lte_ip: IPvAnyAddress
    enodeb_id: int


class NEName(BaseModel):
    ne_name: Annotated[str, Field(min_length=3)]


class NEID(BaseModel):
    id: int