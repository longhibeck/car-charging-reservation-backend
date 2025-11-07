import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    connectors = relationship(
        "Connector", back_populates="car", cascade="all, delete-orphan"
    )
    battery_charge_limit = Column(Integer, default=80, nullable=False)
    battery_size = Column(Integer, nullable=False)
    max_kw_ac = Column(Integer, nullable=False)
    max_kw_dc = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="cars")


class ConnectorType(enum.Enum):
    TYPE_2 = "Type 2"
    SCHUCO = "Schuko"
    CCS = "CCS"
    CHADEMO = "CHAdeMO"


class Connector(Base):
    __tablename__ = "connector"

    id = Column(Integer, primary_key=True)
    type = Column(Enum(ConnectorType), nullable=False)
    car_id = Column(Integer, ForeignKey("car.id"))
    car = relationship("Car", back_populates="connectors")
