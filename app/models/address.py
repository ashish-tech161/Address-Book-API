"""
SQLAlchemy database models
"""
from sqlalchemy import Column, Integer, String
from app.db import Base


class Address(Base):
    """Address model"""
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    
    def __repr__(self):
        return f"<Address(id={self.id}, name='{self.name}')>"
