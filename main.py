from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base
from schemas import AddressCreate, AddressUpdate, AddressResponse
from crud import (
    create_address,
    update_address,
    delete_address,
    get_addresses_within_radius
)
from logger import logger

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Address Book API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/addresses", response_model=AddressResponse)
def add_address(address: AddressCreate, db: Session = Depends(get_db)):
    logger.info("Creating new address")
    return create_address(db, address)

@app.put("/addresses/{address_id}", response_model=AddressResponse)
def edit_address(address_id: int, address: AddressUpdate, db: Session = Depends(get_db)):
    result = update_address(db, address_id, address)
    if not result:
        raise HTTPException(status_code=404, detail="Address not found")
    return result

@app.delete("/addresses/{address_id}")
def remove_address(address_id: int, db: Session = Depends(get_db)):
    result = delete_address(db, address_id)
    if not result:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address deleted"}

@app.get("/addresses/nearby", response_model=list[AddressResponse])
def nearby_addresses(
    latitude: str,
    longitude: str,
    distance_km: float,
    db: Session = Depends(get_db)
):
    return get_addresses_within_radius(db, latitude, longitude, distance_km)
