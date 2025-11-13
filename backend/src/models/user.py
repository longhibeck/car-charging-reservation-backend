import uuid

from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    external_user_id: Mapped[int] = mapped_column(Integer, unique=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    cars: Mapped[list["Car"]] = relationship("Car", back_populates="owner")
