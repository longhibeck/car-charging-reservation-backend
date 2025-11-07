from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    external_user_id = Column(Integer, unique=True)
    username = Column(String, unique=True)
    cars = relationship("Car", back_populates="owner")
