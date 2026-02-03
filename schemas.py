from pydantic import BaseModel, Field

class AddressCreate(BaseModel):
    name: str
    latitude: str
    longitude: str

class AddressUpdate(AddressCreate):
    pass

class AddressResponse(AddressCreate):
    id: int

    class Config:
        from_attributes = True
