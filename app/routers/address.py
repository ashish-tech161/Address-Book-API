"""
Address router - HTTP layer only
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import AddressCreate, AddressUpdate, AddressResponse
from app.services.address_service import AddressService
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.post(
    "",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new address",
    description="Add a new address to the address book"
)
def create_address(
    address: AddressCreate,
    db: Session = Depends(get_db)
) -> AddressResponse:
    """
    Create a new address
    
    - **name**: Name of the address
    - **latitude**: Latitude coordinate
    - **longitude**: Longitude coordinate
    """
    logger.info(f"POST /addresses - Creating address: {address.name}")
    try:
        result = AddressService.create_address(db, address)
        logger.info(f"Address created successfully with ID: {result.id}")
        return result
    except Exception as e:
        logger.error(f"Error creating address: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create address"
        )


@router.get(
    "",
    response_model=List[AddressResponse],
    summary="Get all addresses",
    description="Retrieve all addresses with optional pagination"
)
def list_addresses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[AddressResponse]:
    """
    Get all addresses
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    logger.info(f"GET /addresses - Fetching addresses (skip={skip}, limit={limit})")
    try:
        addresses = AddressService.get_all_addresses(db, skip=skip, limit=limit)
        return addresses
    except Exception as e:
        logger.error(f"Error fetching addresses: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch addresses"
        )


@router.get(
    "/nearby",
    response_model=List[AddressResponse],
    summary="Find nearby addresses",
    description="Find all addresses within a specified radius from given coordinates"
)
def find_nearby_addresses(
    latitude: str,
    longitude: str,
    distance_km: float,
    db: Session = Depends(get_db)
) -> List[AddressResponse]:
    """
    Find nearby addresses
    
    - **latitude**: Center point latitude
    - **longitude**: Center point longitude
    - **distance_km**: Radius in kilometers
    """
    logger.info(
        f"GET /addresses/nearby - Searching within {distance_km}km of ({latitude}, {longitude})"
    )
    
    try:
        addresses = AddressService.find_nearby_addresses(
            db, latitude, longitude, distance_km
        )
        logger.info(f"Found {len(addresses)} nearby addresses")
        return addresses
    except ValueError as e:
        logger.error(f"Invalid input: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error searching nearby addresses: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search nearby addresses"
        )


@router.get(
    "/{address_id}",
    response_model=AddressResponse,
    summary="Get address by ID",
    description="Retrieve a specific address by its ID"
)
def get_address(
    address_id: int,
    db: Session = Depends(get_db)
) -> AddressResponse:
    """
    Get an address by ID
    
    - **address_id**: The ID of the address to retrieve
    """
    logger.info(f"GET /addresses/{address_id} - Fetching address")
    address = AddressService.get_address(db, address_id)
    if not address:
        logger.warning(f"Address with ID {address_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address with ID {address_id} not found"
        )
    return address


@router.put(
    "/{address_id}",
    response_model=AddressResponse,
    summary="Update an address",
    description="Update an existing address by its ID"
)
def update_address(
    address_id: int,
    address: AddressUpdate,
    db: Session = Depends(get_db)
) -> AddressResponse:
    """
    Update an address
    
    - **address_id**: The ID of the address to update
    - **name**: (Optional) Updated name
    - **latitude**: (Optional) Updated latitude
    - **longitude**: (Optional) Updated longitude
    """
    logger.info(f"PUT /addresses/{address_id} - Updating address")
    try:
        result = AddressService.update_address(db, address_id, address)
        if not result:
            logger.warning(f"Address with ID {address_id} not found for update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Address with ID {address_id} not found"
            )
        logger.info(f"Address {address_id} updated successfully")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating address: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update address"
        )


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an address",
    description="Delete an address by its ID"
)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db)
) -> dict:
    """
    Delete an address
    
    - **address_id**: The ID of the address to delete
    """
    logger.info(f"DELETE /addresses/{address_id} - Deleting address")
    try:
        result = AddressService.delete_address(db, address_id)
        if not result:
            logger.warning(f"Address with ID {address_id} not found for deletion")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Address with ID {address_id} not found"
            )
        logger.info(f"Address {address_id} deleted successfully")
        return {"message": "Address deleted successfully", "id": address_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting address: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete address"
        )
