from typing import List

from pydantic import BaseModel, ConfigDict


class ConnectorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str

    @classmethod
    def model_validate_connector(cls, connector):
        """Custom validation for connector objects"""
        return cls(
            id=connector.id,
            type=connector.type.value
            if hasattr(connector.type, "value")
            else str(connector.type),
        )


class CarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    connectors: List[ConnectorResponse]
    battery_charge_limit: int
    battery_size: int
    max_kw_ac: int
    max_kw_dc: int

    @classmethod
    def model_validate_car(cls, car):
        """Custom validation for car objects"""
        return cls(
            id=car.id,
            name=car.name,
            connectors=[
                ConnectorResponse.model_validate_connector(c) for c in car.connectors
            ],
            battery_charge_limit=car.battery_charge_limit,
            battery_size=car.battery_size,
            max_kw_ac=car.max_kw_ac,
            max_kw_dc=car.max_kw_dc,
        )


class CarCreateRequest(BaseModel):
    name: str
    connector_types: List[str]
    battery_charge_limit: int = 80
    battery_size: int
    max_kw_ac: int
    max_kw_dc: int
