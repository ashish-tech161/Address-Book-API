import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from database import Base
from utils import parse_coordinate, haversine

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_addresses.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test and drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ============== Utils Tests ==============

class TestParseCoordinate:
    """Tests for the parse_coordinate function."""

    def test_parse_numeric_float(self):
        """Test parsing a float value."""
        assert parse_coordinate(22.705435) == 22.705435

    def test_parse_numeric_int(self):
        """Test parsing an integer value."""
        assert parse_coordinate(22) == 22.0

    def test_parse_string_plain(self):
        """Test parsing a plain string coordinate."""
        assert parse_coordinate("22.705435") == 22.705435

    def test_parse_string_with_degree_north(self):
        """Test parsing coordinate with degree symbol and N direction."""
        assert parse_coordinate("22.705435° N") == 22.705435

    def test_parse_string_with_degree_south(self):
        """Test parsing coordinate with degree symbol and S direction (should be negative)."""
        assert parse_coordinate("22.705435° S") == -22.705435

    def test_parse_string_with_degree_east(self):
        """Test parsing coordinate with degree symbol and E direction."""
        assert parse_coordinate("75.84361° E") == 75.84361

    def test_parse_string_with_degree_west(self):
        """Test parsing coordinate with degree symbol and W direction (should be negative)."""
        assert parse_coordinate("75.84361° W") == -75.84361

    def test_parse_string_lowercase_direction(self):
        """Test parsing with lowercase direction."""
        assert parse_coordinate("22.705435° n") == 22.705435
        assert parse_coordinate("22.705435° s") == -22.705435


class TestHaversine:
    """Tests for the haversine distance calculation function."""

    def test_same_location(self):
        """Distance between same points should be 0."""
        distance = haversine(22.705435, 75.84361, 22.705435, 75.84361)
        assert distance == 0.0

    def test_known_distance(self):
        """Test distance between two known points (Indore to Bhopal approx 170 km)."""
        # Indore: 22.7196° N, 75.8577° E
        # Bhopal: 23.2599° N, 77.4126° E
        distance = haversine(22.7196, 75.8577, 23.2599, 77.4126)
        assert 165 < distance < 175  # Approximately 170 km

    def test_with_string_coordinates(self):
        """Test haversine with string coordinates."""
        distance = haversine("22.705435° N", "75.84361° E", "22.705435° N", "75.84361° E")
        assert distance == 0.0

    def test_short_distance(self):
        """Test a short distance calculation."""
        # Two points about 1 km apart
        distance = haversine(22.7000, 75.8400, 22.7090, 75.8400)
        assert 0.9 < distance < 1.1


# ============== API Endpoint Tests ==============

class TestCreateAddress:
    """Tests for POST /addresses endpoint."""

    def test_create_address_success(self):
        """Test creating a new address."""
        response = client.post("/addresses", json={
            "name": "Test Location",
            "latitude": "22.705435",
            "longitude": "75.84361"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Location"
        assert data["latitude"] == "22.705435"
        assert data["longitude"] == "75.84361"
        assert "id" in data

    def test_create_address_with_degree_format(self):
        """Test creating address with degree format coordinates."""
        response = client.post("/addresses", json={
            "name": "Indore Office",
            "latitude": "22.705435° N",
            "longitude": "75.84361° E"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Indore Office"

    def test_create_multiple_addresses(self):
        """Test creating multiple addresses."""
        for i in range(3):
            response = client.post("/addresses", json={
                "name": f"Location {i}",
                "latitude": f"22.{700 + i}",
                "longitude": f"75.{840 + i}"
            })
            assert response.status_code == 200


class TestUpdateAddress:
    """Tests for PUT /addresses/{id} endpoint."""

    def test_update_address_success(self):
        """Test updating an existing address."""
        # Create an address first
        create_response = client.post("/addresses", json={
            "name": "Original Name",
            "latitude": "22.705435",
            "longitude": "75.84361"
        })
        address_id = create_response.json()["id"]

        # Update the address
        response = client.put(f"/addresses/{address_id}", json={
            "name": "Updated Name",
            "latitude": "22.710000",
            "longitude": "75.850000"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["latitude"] == "22.710000"

    def test_update_nonexistent_address(self):
        """Test updating a non-existent address returns 404."""
        response = client.put("/addresses/9999", json={
            "name": "Updated Name",
            "latitude": "22.710000",
            "longitude": "75.850000"
        })
        assert response.status_code == 404
        assert response.json()["detail"] == "Address not found"


class TestDeleteAddress:
    """Tests for DELETE /addresses/{id} endpoint."""

    def test_delete_address_success(self):
        """Test deleting an existing address."""
        # Create an address first
        create_response = client.post("/addresses", json={
            "name": "To Delete",
            "latitude": "22.705435",
            "longitude": "75.84361"
        })
        address_id = create_response.json()["id"]

        # Delete the address
        response = client.delete(f"/addresses/{address_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Address deleted"

    def test_delete_nonexistent_address(self):
        """Test deleting a non-existent address returns 404."""
        response = client.delete("/addresses/9999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Address not found"


class TestNearbyAddresses:
    """Tests for GET /addresses/nearby endpoint."""

    def test_nearby_addresses_empty(self):
        """Test nearby addresses with no data."""
        response = client.get("/addresses/nearby", params={
            "latitude": 22.700,
            "longitude": 75.840,
            "distance_km": 5
        })
        assert response.status_code == 200
        assert response.json() == []

    def test_nearby_addresses_finds_nearby(self):
        """Test that nearby addresses are found within radius."""
        # Create addresses
        client.post("/addresses", json={
            "name": "Nearby Location",
            "latitude": "22.705",
            "longitude": "75.844"
        })
        client.post("/addresses", json={
            "name": "Far Location",
            "latitude": "23.500",
            "longitude": "76.500"
        })

        # Search for nearby addresses
        response = client.get("/addresses/nearby", params={
            "latitude": 22.700,
            "longitude": 75.840,
            "distance_km": 5
        })
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Nearby Location"

    def test_nearby_addresses_with_string_coords(self):
        """Test nearby with string coordinate query params."""
        client.post("/addresses", json={
            "name": "Test Location",
            "latitude": "22.705435° N",
            "longitude": "75.84361° E"
        })

        response = client.get("/addresses/nearby", params={
            "latitude": "22.700",
            "longitude": "75.840",
            "distance_km": 5
        })
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_nearby_addresses_large_radius(self):
        """Test nearby with large radius finds all addresses."""
        # Create multiple addresses
        for i in range(3):
            client.post("/addresses", json={
                "name": f"Location {i}",
                "latitude": f"22.{700 + i}",
                "longitude": f"75.{840 + i}"
            })

        response = client.get("/addresses/nearby", params={
            "latitude": 22.700,
            "longitude": 75.840,
            "distance_km": 100
        })
        assert response.status_code == 200
        assert len(response.json()) == 3
