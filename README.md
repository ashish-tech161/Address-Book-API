# Address Book API

A FastAPI-based REST API for managing addresses with geolocation support. Find nearby addresses using the Haversine formula for distance calculation.

## Documentation

For a detailed explanation of the project architecture, design decisions, and implementation strategy, please refer to the [Approach Document](docs/Address_Book_API_Approach_Document.pdf).

## Features

- Create, update, and delete addresses
- Store addresses with latitude/longitude coordinates
- Find nearby addresses within a specified radius
- Supports coordinate formats like `"22.705435° N"` or plain numbers
- SQLite database for data persistence
- **Comprehensive logging system** with structured logging, request/response logging, and log rotation
- **Proper FastAPI project structure** following best practices
- Environment-based configuration
- API versioning support

## Installation

### 1. Clone/Navigate to the project directory

```bash
cd Address_Book_API
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv myenv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment (optional)

Copy `.env.example` to `.env` and modify settings as needed:

```bash
cp .env.example .env
```

## Running the API

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at: **http://127.0.0.1:8000**

### API Documentation

Once running, access the interactive API docs:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **OpenAPI JSON**: http://127.0.0.1:8000/openapi.json

## API Endpoints

All endpoints are prefixed with `/api/v1`

### 1. Create Address

**POST** `/api/v1/addresses`

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/addresses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Indore Office",
    "latitude": "22.705435° N",
    "longitude": "75.84361° E"
  }'
```

**Or with plain numbers:**

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/addresses" \
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

### 2. Get All Addresses

**GET** `/api/v1/addresses`

Query Parameters:
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

```bash
curl "http://127.0.0.1:8000/api/v1/addresses?skip=0&limit=10"
```

---

### 3. Get Address by ID

**GET** `/api/v1/addresses/{address_id}`

```bash
curl "http://127.0.0.1:8000/api/v1/addresses/1"
```

---

### 4. Update Address

**PUT** `/api/v1/addresses/{address_id}`

```bash
curl -X PUT "http://127.0.0.1:8000/api/v1/addresses/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Office Name",
    "latitude": "22.710000",
    "longitude": "75.850000"
  }'
```

**Note:** All fields are optional in the update request.

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

### 5. Delete Address

**DELETE** `/api/v1/addresses/{address_id}`

```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/addresses/1"
```

**Response:**
```json
{
  "message": "Address deleted successfully",
  "id": 1
}
```

---

### 6. Find Nearby Addresses

**GET** `/api/v1/addresses/nearby`

Query Parameters:
- `latitude` (required): Latitude of the center point
- `longitude` (required): Longitude of the center point
- `distance_km` (required): Search radius in kilometers

```bash
curl "http://127.0.0.1:8000/api/v1/addresses/nearby?latitude=22.700&longitude=75.840&distance_km=5"
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

---

### 7. Health Check

**GET** `/health`

```bash
curl "http://127.0.0.1:8000/health"
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

## Logging

The application includes comprehensive logging:

### Log Configuration

- **Log Level**: Configurable via `LOG_LEVEL` environment variable (default: `INFO`)
- **Log Format**: JSON (for production) or Text (for development) via `LOG_FORMAT`
- **Log Files**: Rotating file handler with configurable size and backup count
- **Request/Response Logging**: Automatic logging of all HTTP requests and responses

### Log Locations

- **Console**: All logs are output to stdout/stderr
- **File**: Logs are written to `logs/app.log` (configurable via `LOG_FILE`)

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages
- **ERROR**: Error messages with stack traces

### Example Log Output

**Text Format (Development):**
```
2024-01-15 10:30:45 | INFO     | app.api.v1.endpoints.addresses | add_address:28 | POST /api/v1/addresses - Creating address: Indore Office
2024-01-15 10:30:45 | INFO     | app.core.middleware | dispatch:30 | Response: POST /api/v1/addresses - 201
```

**JSON Format (Production):**
```json
{"timestamp": "2024-01-15T10:30:45.123456", "level": "INFO", "logger": "app.api.v1.endpoints.addresses", "message": "POST /api/v1/addresses - Creating address: Indore Office", "module": "addresses", "function": "add_address", "line": 28}
```

## Running Unit Tests

The project includes comprehensive unit tests using pytest.

### Run all tests

```bash
python -m pytest tests/ -v
```

### Run with coverage

```bash
python -m pytest tests/ --cov=app --cov-report=html
```

## Project Structure

```
Address_Book_API/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application initialization
│   ├── utils.py             # Utility functions (haversine, coordinate parsing)
│   ├── api/
│   │   └── v1/
│   │       ├── api.py       # API v1 router
│   │       └── endpoints/
│   │           └── addresses.py  # Address endpoints
│   ├── core/
│   │   ├── config.py        # Application configuration
│   │   ├── logging.py       # Logging configuration
│   │   └── middleware.py    # Custom middleware (request/response logging)
│   ├── db/
│   │   ├── __init__.py      # Database session & engine exports
│   │   └── database.py      # SQLAlchemy configuration
│   ├── models/              # Database models
│   ├── routers/             # API routes
│   ├── schemas/             # Pydantic schemas
│   └── services/            # Business logic (combined with data access)
├── tests/
│   └── test_api.py          # Unit tests for API and utilities
├── docs/                    # Documentation files
├── logs/                    # Log files (auto-created)
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Configuration

Configuration is managed through environment variables. See `.env.example` for available options:

- `ENVIRONMENT`: Application environment (development, staging, production)
- `DEBUG`: Enable debug mode
- `DATABASE_URL`: Database connection string
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `LOG_FORMAT`: Log format (json or text)
- `LOG_FILE`: Path to log file
- `API_V1_STR`: API version prefix (default: `/api/v1`)

## Coordinate Format Support

The API supports various coordinate formats:

| Format | Example |
|--------|---------|
| Degrees with direction | `"22.705435° N"`, `"75.84361° E"` |
| Plain decimal | `"22.705435"`, `"75.84361"` |
| Negative for S/W | `"-22.705435"`, `"-75.84361"` |

**Note:** South (S) and West (W) coordinates are automatically converted to negative values.

## Best Practices Implemented

 **Project Structure**: Proper FastAPI project structure with separation of concerns  
 **Logging**: Comprehensive logging with structured logging support  
 **Error Handling**: Proper exception handling with detailed error messages  
 **API Versioning**: Versioned API endpoints (`/api/v1`)  
 **Configuration Management**: Environment-based configuration  
 **Type Hints**: Full type annotations throughout the codebase  
 **Documentation**: Comprehensive API documentation with Swagger/ReDoc  
 **Testing**: Unit tests for all endpoints and utilities  
 **Database**: Proper session management with dependency injection  

## Troubleshooting

### Module not found error
Make sure you're running uvicorn from the project directory:
```bash
cd Address_Book_API
uvicorn main:app --reload
```

### Logs directory not found
The logs directory will be created automatically. If you encounter issues, create it manually:
```bash
mkdir -p logs
```

## License

MIT License
