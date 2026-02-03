# Address Book API

A FastAPI-based REST API for managing addresses with geolocation support. Find nearby addresses using the Haversine formula for distance calculation.

## Features

- ✅ Create, update, and delete addresses
- ✅ Store addresses with latitude/longitude coordinates
- ✅ Find nearby addresses within a specified radius
- ✅ Supports coordinate formats like `"22.705435° N"` or plain numbers
- ✅ SQLite database for data persistence
- ✅ Logging for debugging and monitoring

## Installation

### 1. Clone/Navigate to the project directory

```bash
cd /home/tw-hp/Desktop/task/Address-Book-API
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the API

Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at: **http://127.0.0.1:8000**

### API Documentation

Once running, access the interactive API docs:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### 1. Create Address

**POST** `/addresses`

```bash
curl -X POST "http://127.0.0.1:8000/addresses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Indore Office",
    "latitude": "22.705435° N",
    "longitude": "75.84361° E"
  }'
```

**Or with plain numbers:**

```bash
curl -X POST "http://127.0.0.1:8000/addresses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Indore Office",
    "latitude": "22.705435",
    "longitude": "75.84361"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Indore Office",
  "latitude": "22.705435° N",
  "longitude": "75.84361° E"
}
```

---

### 2. Update Address

**PUT** `/addresses/{address_id}`

```bash
curl -X PUT "http://127.0.0.1:8000/addresses/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Office Name",
    "latitude": "22.710000",
    "longitude": "75.850000"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Updated Office Name",
  "latitude": "22.710000",
  "longitude": "75.850000"
}
```

---

### 3. Delete Address

**DELETE** `/addresses/{address_id}`

```bash
curl -X DELETE "http://127.0.0.1:8000/addresses/1"
```

**Response:**
```json
{
  "message": "Address deleted"
}
```

---

### 4. Find Nearby Addresses

**GET** `/addresses/nearby`

Query Parameters:
- `latitude` (required): Latitude of the center point
- `longitude` (required): Longitude of the center point
- `distance_km` (required): Search radius in kilometers

```bash
curl "http://127.0.0.1:8000/addresses/nearby?latitude=22.700&longitude=75.840&distance_km=5"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Indore Office",
    "latitude": "22.705435° N",
    "longitude": "75.84361° E"
  },
  {
    "id": 2,
    "name": "Nearby Location",
    "latitude": "22.702000",
    "longitude": "75.838000"
  }
]
```

## Running Unit Tests

The project includes comprehensive unit tests using pytest.

### Install test dependencies

```bash
pip install pytest httpx
```

### Run all tests

```bash
# Set PYTHONPATH to current directory to resolve imports
export PYTHONPATH=$PYTHONPATH:.
python -m pytest tests/ -v
```

## Project Structure

```
Address-Book-API/
├── main.py          # FastAPI application & routes
├── database.py      # SQLAlchemy database setup
├── models.py        # Database models
├── schemas.py       # Pydantic schemas for validation
├── crud.py          # Database CRUD operations
├── utils.py         # Utility functions (haversine, coordinate parsing)
├── logger.py        # Logging configuration
├── tests/
│   └── test_api.py      # Unit tests for API and utilities
├── requirements.txt     # Python dependencies
├── addresses.db         # SQLite database (auto-created)
└── README.md            # This file
```

## Coordinate Format Support

The API supports various coordinate formats:

| Format | Example |
|--------|---------|
| Degrees with direction | `"22.705435° N"`, `"75.84361° E"` |
| Plain decimal | `"22.705435"`, `"75.84361"` |
| Negative for S/W | `"-22.705435"`, `"-75.84361"` |

**Note:** South (S) and West (W) coordinates are automatically converted to negative values.

## Troubleshooting

### Module not found error
Make sure you're running uvicorn from the project directory:
```bash
cd /home/tw-hp/Desktop/task/Address-Book-API
uvicorn main:app --reload
```

## License

MIT License
