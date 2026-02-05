"""
CRUD operations for addresses
"""
from typing import Optional, Union, List
from sqlalchemy.orm import Session
from app.models import Address
from app.schemas import AddressCreate, AddressUpdate
from app.utils import haversine
from app.core.logging import get_logger

logger = get_logger(__name__)


def create_address(db: Session, address: AddressCreate) -> Address:
    """
    Create a new address
    
    Args:
        db: Database session
        address: Address data
        
    Returns:
        Created address
    """
    logger.info(f"Creating new address: {address.name}")
    try:
        db_address = Address(**address.model_dump())
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        logger.info(f"Address created successfully with ID: {db_address.id}")
        return db_address
    except Exception as e:
        logger.error(f"Error creating address: {e}", exc_info=True)
        db.rollback()
        raise


def get_address(db: Session, address_id: int) -> Optional[Address]:
    """
    Get an address by ID
    
    Args:
        db: Database session
        address_id: Address ID
        
    Returns:
        Address if found, None otherwise
    """
    logger.debug(f"Fetching address with ID: {address_id}")
    address = db.query(Address).filter(Address.id == address_id).first()
    if address:
        logger.debug(f"Address found: {address.name}")
    else:
        logger.warning(f"Address with ID {address_id} not found")
    return address


def get_all_addresses(db: Session, skip: int = 0, limit: int = 100) -> List[Address]:
    """
    Get all addresses with pagination
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of addresses
    """
    logger.debug(f"Fetching addresses (skip={skip}, limit={limit})")
    addresses = db.query(Address).offset(skip).limit(limit).all()
    logger.info(f"Retrieved {len(addresses)} addresses")
    return addresses


def update_address(db: Session, address_id: int, address: AddressUpdate) -> Optional[Address]:
    """
    Update an address
    
    Args:
        db: Database session
        address_id: Address ID
        address: Updated address data
        
    Returns:
        Updated address if found, None otherwise
    """
    logger.info(f"Updating address with ID: {address_id}")
    db_address = db.query(Address).filter(Address.id == address_id).first()
    
    if not db_address:
        logger.warning(f"Address with ID {address_id} not found for update")
        return None
    
    try:
        update_data = address.model_dump(exclude_unset=True)
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


def delete_address(db: Session, address_id: int) -> Optional[Address]:
    """
    Delete an address
    
    Args:
        db: Database session
        address_id: Address ID
        
    Returns:
        Deleted address if found, None otherwise
    """
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


def get_addresses_within_radius(
    db: Session,
    latitude: Union[str, float],
    longitude: Union[str, float],
    distance_km: float
) -> List[Address]:
    """
    Get all addresses within a specified radius
    
    Args:
        db: Database session
        latitude: Center point latitude
        longitude: Center point longitude
        distance_km: Radius in kilometers
        
    Returns:
        List of addresses within radius, sorted by distance
    """
    logger.info(
        f"Searching for addresses within {distance_km}km of ({latitude}, {longitude})"
    )
    
    try:
        addresses = db.query(Address).all()
        logger.debug(f"Found {len(addresses)} total addresses to filter")
        
        nearby_with_dist = []
        
        for addr in addresses:
            try:
                dist = haversine(latitude, longitude, addr.latitude, addr.longitude)
                if 0 <= dist <= distance_km:
                    nearby_with_dist.append((addr, dist))
                    logger.debug(f"Address {addr.id} ({addr.name}) is {dist:.2f}km away")
            except Exception as e:
                logger.warning(
                    f"Error calculating distance for address {addr.id}: {e}",
                    exc_info=True
                )
                continue
        
        # Sort by distance (closest first)
        nearby_with_dist.sort(key=lambda x: x[1])
        
        result = [item[0] for item in nearby_with_dist]
        logger.info(f"Found {len(result)} addresses within {distance_km}km")
        
        return result
        
    except Exception as e:
        logger.error(f"Error searching addresses within radius: {e}", exc_info=True)
        raise
