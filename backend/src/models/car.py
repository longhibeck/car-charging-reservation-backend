import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    connectors = relationship(
        "Connector", back_populates="car", cascade="all, delete-orphan"
    )
    battery_charge_limit: Mapped[int] = mapped_column(
        Integer, default=80, nullable=False
    )
    battery_size: Mapped[int] = mapped_column(Integer, nullable=False)
    max_kw_ac: Mapped[int] = mapped_column(Integer, nullable=False)
    max_kw_dc: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id")
    )
    owner: Mapped["User"] = relationship("User", back_populates="cars")


class ConnectorType(enum.Enum):
    TYPE_2 = "Type-2"
    SCHUKO = "Schuko"
    CCS = "CCS"
    CHADEMO = "CHAdeMO"


class Connector(Base):
    __tablename__ = "connectors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    type: Mapped[ConnectorType] = mapped_column(Enum(ConnectorType), nullable=False)
    car_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cars.id"))
    car: Mapped["Car"] = relationship("Car", back_populates="connectors")
