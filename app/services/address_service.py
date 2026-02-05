"""
Address business logic service and data access
"""
from typing import Optional, List, Union
from sqlalchemy.orm import Session

from app.models import Address
from app.schemas import AddressCreate, AddressUpdate
from app.utils import haversine
from app.core.logging import get_logger

logger = get_logger(__name__)


class AddressService:
    """Service layer for address management"""
    
    @staticmethod
    def create_address(db: Session, address_data: AddressCreate) -> Address:
        """Create a new address"""
        logger.info(f"Creating new address: {address_data.name}")
        try:
            db_address = Address(**address_data.model_dump())
            db.add(db_address)
            db.commit()
            db.refresh(db_address)
            logger.info(f"Address created successfully with ID: {db_address.id}")
            return db_address
        except Exception as e:
            logger.error(f"Error creating address: {e}", exc_info=True)
            db.rollback()
            raise

    @staticmethod
    def get_address(db: Session, address_id: int) -> Optional[Address]:
        """Get an address by ID"""
        logger.debug(f"Fetching address with ID: {address_id}")
        return db.query(Address).filter(Address.id == address_id).first()

    @staticmethod
    def get_all_addresses(db: Session, skip: int = 0, limit: int = 100) -> List[Address]:
        """Get all addresses with pagination"""
        logger.debug(f"Fetching addresses (skip={skip}, limit={limit})")
        return db.query(Address).offset(skip).limit(limit).all()

    @staticmethod
    def update_address(db: Session, address_id: int, address_data: AddressUpdate) -> Optional[Address]:
        """Update an address"""
        logger.info(f"Updating address with ID: {address_id}")
        db_address = db.query(Address).filter(Address.id == address_id).first()
        
        if not db_address:
            logger.warning(f"Address with ID {address_id} not found for update")
            return None
        
        try:
            update_data = address_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_address, key, value)
            
            db.commit()
            db.refresh(db_address)
            logger.info(f"Address {address_id} updated successfully")
            return db_address
        except Exception as e:
            logger.error(f"Error updating address {address_id}: {e}", exc_info=True)
            db.rollback()
            raise

    @staticmethod
    def delete_address(db: Session, address_id: int) -> Optional[Address]:
        """Delete an address"""
        logger.info(f"Deleting address with ID: {address_id}")
        db_address = db.query(Address).filter(Address.id == address_id).first()
        
        if not db_address:
            logger.warning(f"Address with ID {address_id} not found for deletion")
            return None
        
        try:
            db.delete(db_address)
            db.commit()
            logger.info(f"Address {address_id} deleted successfully")
            return db_address
        except Exception as e:
            logger.error(f"Error deleting address {address_id}: {e}", exc_info=True)
            db.rollback()
            raise

    @staticmethod
    def find_nearby_addresses(
        db: Session,
        latitude: Union[str, float],
        longitude: Union[str, float],
        distance_km: float
    ) -> List[Address]:
        """Find nearby addresses within a specified radius"""
        logger.info(f"Finding addresses within {distance_km}km of ({latitude}, {longitude})")
        
        if distance_km <= 0:
            raise ValueError("distance_km must be greater than 0")
        
        try:
            addresses = db.query(Address).all()
            nearby_with_dist = []
            
            for addr in addresses:
                try:
                    dist = haversine(latitude, longitude, addr.latitude, addr.longitude)
                    if 0 <= dist <= distance_km:
                        nearby_with_dist.append((addr, dist))
                except Exception as e:
                    logger.warning(f"Error calculating distance for address {addr.id}: {e}")
                    continue
            
            # Sort by distance
            nearby_with_dist.sort(key=lambda x: x[1])
            return [item[0] for item in nearby_with_dist]
            
        except Exception as e:
            logger.error(f"Error searching nearby addresses: {e}", exc_info=True)
            raise
