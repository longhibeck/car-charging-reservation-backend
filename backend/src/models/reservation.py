import uuid
from datetime import datetime, timezone
from enum import StrEnum

from sqlalchemy import UUID, CheckConstraint, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class ReservationStatus(StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Reservation(Base):
    __tablename__ = "reservations"

    # Add the constraint at the table level
    __table_args__ = (
        CheckConstraint("start_time < end_time", name="check_valid_time_range"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Time fields
    start_time: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    end_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    # Reservation details
    status: Mapped[ReservationStatus] = mapped_column(
        Enum(ReservationStatus, name="reservationstatus"),
        default=ReservationStatus.ACTIVE,
        nullable=False,
    )

    # External charging point - just store the ID as string
    charging_point_id: Mapped[str] = mapped_column(String, nullable=False)

    # Foreign Keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    car_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cars.id"), nullable=False
    )
