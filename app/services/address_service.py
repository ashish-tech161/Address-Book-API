"""
Address business logic service
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models import Address
from app.schemas import AddressCreate, AddressUpdate
from app.crud import (
    create_address as crud_create_address,
    get_address as crud_get_address,
    get_all_addresses as crud_get_all_addresses,
    update_address as crud_update_address,
    delete_address as crud_delete_address,
    get_addresses_within_radius as crud_get_addresses_within_radius
)
from app.core.logging import get_logger

logger = get_logger(__name__)


class AddressService:
    """Service layer for address business logic"""
    
    @staticmethod
    def create_address(db: Session, address_data: AddressCreate) -> Address:
        """
        Create a new address
        
        Args:
            db: Database session
            address_data: Address creation data
            
        Returns:
            Created address
            
        Raises:
            Exception: If address creation fails
        """
        logger.info(f"Service: Creating address: {address_data.name}")
        try:
            address = crud_create_address(db, address_data)
            logger.info(f"Service: Address created successfully with ID: {address.id}")
            return address
        except Exception as e:
            logger.error(f"Service: Error creating address: {e}", exc_info=True)
            raise
    
    @staticmethod
    def get_address(db: Session, address_id: int) -> Optional[Address]:
        """
        Get an address by ID
        
        Args:
            db: Database session
            address_id: Address ID
            
        Returns:
            Address if found, None otherwise
        """
        logger.debug(f"Service: Fetching address with ID: {address_id}")
        return crud_get_address(db, address_id)
    
    @staticmethod
    def get_all_addresses(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[Address]:
        """
        Get all addresses with pagination
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of addresses
        """
        logger.debug(f"Service: Fetching addresses (skip={skip}, limit={limit})")
        addresses = crud_get_all_addresses(db, skip=skip, limit=limit)
        logger.info(f"Service: Retrieved {len(addresses)} addresses")
        return addresses
    
    @staticmethod
    def update_address(
        db: Session,
        address_id: int,
        address_data: AddressUpdate
    ) -> Optional[Address]:
        """
        Update an address
        
        Args:
            db: Database session
            address_id: Address ID
            address_data: Updated address data
            
        Returns:
            Updated address if found, None otherwise
            
        Raises:
            Exception: If address update fails
        """
        logger.info(f"Service: Updating address with ID: {address_id}")
        try:
            address = crud_update_address(db, address_id, address_data)
            if address:
                logger.info(f"Service: Address {address_id} updated successfully")
            return address
        except Exception as e:
            logger.error(f"Service: Error updating address {address_id}: {e}", exc_info=True)
            raise
    
    @staticmethod
    def delete_address(db: Session, address_id: int) -> Optional[Address]:
        """
        Delete an address
        
        Args:
            db: Database session
            address_id: Address ID
            
        Returns:
            Deleted address if found, None otherwise
            
        Raises:
            Exception: If address deletion fails
        """
        logger.info(f"Service: Deleting address with ID: {address_id}")
        try:
            address = crud_delete_address(db, address_id)
            if address:
                logger.info(f"Service: Address {address_id} deleted successfully")
            return address
        except Exception as e:
            logger.error(f"Service: Error deleting address {address_id}: {e}", exc_info=True)
            raise
    
    @staticmethod
    def find_nearby_addresses(
        db: Session,
        latitude: str,
        longitude: str,
        distance_km: float
    ) -> List[Address]:
        """
        Find nearby addresses within a specified radius
        
        Args:
            db: Database session
            latitude: Center point latitude
            longitude: Center point longitude
            distance_km: Radius in kilometers
            
        Returns:
            List of addresses within radius, sorted by distance
            
        Raises:
            ValueError: If coordinates are invalid
            Exception: If search fails
        """
        logger.info(
            f"Service: Finding addresses within {distance_km}km of ({latitude}, {longitude})"
        )
        
        # Validate distance
        if distance_km <= 0:
            raise ValueError("distance_km must be greater than 0")
        
        try:
            addresses = crud_get_addresses_within_radius(
                db, latitude, longitude, distance_km
            )
            logger.info(f"Service: Found {len(addresses)} nearby addresses")
            return addresses
        except ValueError as e:
            logger.error(f"Service: Invalid coordinates: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Service: Error finding nearby addresses: {e}", exc_info=True)
            raise
