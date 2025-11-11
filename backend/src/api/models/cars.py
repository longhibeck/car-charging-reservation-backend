from typing import List

from pydantic import UUID4, BaseModel, ConfigDict

from models.car import ConnectorType


class ConnectorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    type: ConnectorType


class CarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    name: str
    connectors: List[ConnectorResponse]
    battery_charge_limit: int
    battery_size: int
    max_kw_ac: int
    max_kw_dc: int


class CarCreateRequest(BaseModel):
    name: str
    connector_types: List[str]
    battery_charge_limit: int = 80
    battery_size: int
    max_kw_ac: int
    max_kw_dc: int
