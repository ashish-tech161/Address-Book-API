"""
Pydantic schemas for request/response validation
"""
from typing import Optional
from pydantic import BaseModel, Field


class AddressCreate(BaseModel):
    """Schema for creating an address"""
    name: str = Field(..., description="Name of the address", min_length=1)
    latitude: str = Field(..., description="Latitude coordinate")
    longitude: str = Field(..., description="Longitude coordinate")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Home",
                "latitude": "22.705435° N",
                "longitude": "75.84361° E"
            }
        }


class AddressUpdate(BaseModel):
    """Schema for updating an address"""
    name: Optional[str] = Field(None, description="Name of the address", min_length=1)
    latitude: Optional[str] = Field(None, description="Latitude coordinate")
    longitude: Optional[str] = Field(None, description="Longitude coordinate")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Home",
                "latitude": "22.705435° N",
                "longitude": "75.84361° E"
            }
        }


class AddressResponse(BaseModel):
    """Schema for address response"""
    id: int
    name: str
    latitude: str
    longitude: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Home",
                "latitude": "22.705435° N",
                "longitude": "75.84361° E"
            }
        }
