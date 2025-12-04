from pydantic import UUID4, BaseModel, ConfigDict, Field, model_validator

from src.models.car import ConnectorType


class CarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    name: str = Field(description="Car name")
    connector_types: list[ConnectorType] = Field(
        description="List of supported connector types"
    )
    battery_charge_limit: int = Field(
        gt=0, le=100, description="Battery charge limit percentage"
    )
    battery_size: int = Field(gt=0, description="Battery size in kWh")
    max_kw_ac: int = Field(gt=0, description="Maximum AC charging power in kW")
    max_kw_dc: int = Field(gt=0, description="Maximum DC charging power in kW")

    @model_validator(mode="after")
    def sort_connector_types(self) -> "CarResponse":
        if self.connector_types:
            unique_types = list(set(self.connector_types))
            self.connector_types = sorted(unique_types, key=lambda x: x.value)
        return self


class CarCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120, description="Car name")
    connector_types: set[str] = Field(
        min_length=1,
        description="List of connector types",
    )
    battery_charge_limit: int = Field(
        default=80, gt=0, le=100, description="Battery charge limit percentage"
    )
    battery_size: int = Field(gt=0, description="Battery size in kWh")
    max_kw_ac: int = Field(gt=0, description="Maximum AC charging power in kW")
    max_kw_dc: int = Field(gt=0, description="Maximum DC charging power in kW")
