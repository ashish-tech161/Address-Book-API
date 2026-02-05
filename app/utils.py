"""
Utility functions
"""
import math
import re
from typing import Union
from app.core.logging import get_logger

logger = get_logger(__name__)


def parse_coordinate(coord: Union[str, float, int]) -> float:
    """
    Parse coordinate string like '22.705435° N' or '75.84361° E' to float.
    
    Args:
        coord: Coordinate string or numeric value
        
    Returns:
        Parsed coordinate as float
    """
    logger.debug(f"Parsing coordinate: {coord}")
    
    if isinstance(coord, (int, float)):
        logger.debug(f"Coordinate is already numeric: {coord}")
        return float(coord)
    
    # Remove degree symbol and extra spaces
    coord_str = str(coord).strip()
    
    # Extract numeric value and direction
    match = re.match(r"([-+]?\d*\.?\d+)\s*°?\s*([NSEW])?", coord_str, re.IGNORECASE)
    
    if match:
        value = float(match.group(1))
        direction = match.group(2)
        
        # Apply negative sign for South and West
        if direction and direction.upper() in ['S', 'W']:
            value = -value
            logger.debug(f"Applied negative sign for {direction} direction")
        
        logger.info(f"Parsed coordinate '{coord}' to {value}")
        return value
    
    # Fallback: try direct conversion
    logger.warning(f"Using fallback conversion for coordinate: {coord}")
    try:
        return float(coord_str)
    except ValueError as e:
        logger.error(f"Failed to parse coordinate: {coord}", exc_info=True)
        raise ValueError(f"Invalid coordinate format: {coord}") from e


def haversine(lat1: Union[str, float], lon1: Union[str, float], lat2: Union[str, float], lon2: Union[str, float]) -> float:
    """
    Calculate distance between two points using Haversine formula.
    
    Args:
        lat1: Latitude of first point
        lon1: Longitude of first point
        lat2: Latitude of second point
        lon2: Longitude of second point
        
    Returns:
        Distance in kilometers
    """
    logger.info(f"Calculating distance from ({lat1}, {lon1}) to ({lat2}, {lon2})")
    
    try:
        # Parse coordinates if they are strings
        lat1_parsed = parse_coordinate(lat1)
        lon1_parsed = parse_coordinate(lon1)
        lat2_parsed = parse_coordinate(lat2)
        lon2_parsed = parse_coordinate(lon2)
        
        # Validate coordinate ranges
        if not (-90 <= lat1_parsed <= 90) or not (-90 <= lat2_parsed <= 90):
            raise ValueError("Latitude must be between -90 and 90 degrees")
        if not (-180 <= lon1_parsed <= 180) or not (-180 <= lon2_parsed <= 180):
            raise ValueError("Longitude must be between -180 and 180 degrees")
        
        R = 6371  # Earth radius in KM
        d_lat = math.radians(lat2_parsed - lat1_parsed)
        d_lon = math.radians(lon2_parsed - lon1_parsed)

        a = math.sin(d_lat / 2)**2 + \
            math.cos(math.radians(lat1_parsed)) * \
            math.cos(math.radians(lat2_parsed)) * \
            math.sin(d_lon / 2)**2

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        
        logger.info(f"Calculated distance: {distance:.2f} km")
        return distance
        
    except Exception as e:
        logger.error(f"Error calculating haversine distance: {e}", exc_info=True)
        raise
