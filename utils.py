import math
import re
from logger import logger

def parse_coordinate(coord):
    """Parse coordinate string like '22.705435° N' or '75.84361° E' to float."""
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
    return float(coord_str)

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula."""
    logger.info(f"Calculating distance from ({lat1}, {lon1}) to ({lat2}, {lon2})")
    
    # Parse coordinates if they are strings
    lat1 = parse_coordinate(lat1)
    lon1 = parse_coordinate(lon1)
    lat2 = parse_coordinate(lat2)
    lon2 = parse_coordinate(lon2)
    
    R = 6371  # Earth radius in KM
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = math.sin(d_lat / 2)**2 + \
        math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * \
        math.sin(d_lon / 2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    logger.info(f"Calculated distance: {distance:.2f} km")
    return distance
