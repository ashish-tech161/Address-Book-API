from sqlalchemy.orm import Session
from models import Address
from utils import haversine

def create_address(db: Session, address):
    obj = Address(**address.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_address(db: Session, address_id: int, address):
    obj = db.query(Address).filter(Address.id == address_id).first()
    if not obj:
        return None
    for key, value in address.dict().items():
        setattr(obj, key, value)
    db.commit()
    return obj

def delete_address(db: Session, address_id: int):
    obj = db.query(Address).filter(Address.id == address_id).first()
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj

def get_addresses_within_radius(db, lat, lon, distance_km):
    addresses = db.query(Address).all()
    nearby_with_dist = []
    
    for addr in addresses:
        dist = haversine(lat, lon, addr.latitude, addr.longitude)
        if 0 < dist <= distance_km:
            nearby_with_dist.append((addr, dist))
            
    # Sort by distance (closest first)
    nearby_with_dist.sort(key=lambda x: x[1])
    
    return [item[0] for item in nearby_with_dist]
