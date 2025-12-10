import uuid
from enum import StrEnum

from sqlalchemy import ARRAY, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class ConnectorType(StrEnum):
    TYPE_2 = "Type-2"
    SCHUKO = "Schuko"
    CCS = "CCS"
    CHADEMO = "CHAdeMO"


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    connector_types: Mapped[list[ConnectorType]] = mapped_column(
        ARRAY(Enum(ConnectorType)),
        nullable=False,
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
