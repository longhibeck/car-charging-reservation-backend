from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, Field, model_validator

from src.api.models.cars import CarResponse
from src.models.reservation import ReservationStatus


class ReservationBase(BaseModel):
    start_time: datetime = Field(description="Reservation start time")
    end_time: datetime = Field(description="Reservation end time")

    @model_validator(mode="after")
    def validate_times(self) -> "ReservationBase":
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class ReservationCreateRequest(ReservationBase):
    car_id: UUID4 = Field(description="ID of the car to charge")
    charging_point_id: str = Field(description="External charging point ID")


class ReservationResponse(ReservationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    status: ReservationStatus
    charging_point_id: str
    created_at: datetime
    updated_at: datetime

    # Related objects
    car: CarResponse
