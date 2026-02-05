# Architecture Overview

This FastAPI application follows a clean architecture pattern with clear separation of concerns.

## Project Structure

```
app/
├── routers/                # API Layer (HTTP concerns only)
│   ├── __init__.py         # Router aggregation
│   ├── address.py          # Address route handlers
│   └── base.py             # Root and health endpoints
│
├── services/               # Business Logic Layer
│   └── address_service.py  # Business logic for addresses
│
├── crud/                   # Data Access Layer (Repository pattern)
│   └── address.py          # Direct database operations
│
├── models/                 # SQLAlchemy ORM models
│   └── address.py
│
├── schemas/                # Pydantic schemas (request/response)
│   └── address.py
│
├── db/                    # Database configuration
│   └── database.py         # Database engine and session
│
├── dependencies.py         # FastAPI dependencies
├── utils.py                # Utility functions
│
└── core/                   # Core application components
    ├── config.py           # Configuration management
    ├── logging.py          # Logging setup
    └── middleware.py       # Custom middleware
```

## Layer Responsibilities

### 1. API Layer (`app/routers/`)
**Purpose**: Handle HTTP requests and responses only

**Responsibilities**:
- Define route endpoints
- Validate HTTP request/response formats
- Handle HTTP status codes and exceptions
- Call service layer methods
- No business logic

**Example**:
```python
@router.post("", response_model=AddressResponse)
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    return AddressService.create_address(db, address)
```

### 2. Service Layer (`app/services/`)
**Purpose**: Implement business logic

**Responsibilities**:
- Business rules and validation
- Orchestrate multiple CRUD operations
- Handle business exceptions
- Coordinate between different data sources
- No direct HTTP concerns

**Example**:
```python
class AddressService:
    @staticmethod
    def create_address(db: Session, address_data: AddressCreate) -> Address:
        # Business logic here
        # Validation, transformation, etc.
        return crud_create_address(db, address_data)
```

### 3. Data Access Layer (`app/crud.py`)
**Purpose**: Direct database operations

**Responsibilities**:
- CRUD operations
- Database queries
- Transaction management
- No business logic

**Example**:
```python
def create_address(db: Session, address: AddressCreate) -> Address:
    db_address = Address(**address.model_dump())
    db.add(db_address)
    db.commit()
    return db_address
```

## Data Flow

```
HTTP Request
    ↓
Router (app/routers/)
    ↓
Service Layer (app/services/)
    ↓
CRUD Layer (app/crud.py)
    ↓
Database (SQLAlchemy)
```

## Benefits of This Architecture

1. **Separation of Concerns**: Each layer has a single responsibility
2. **Testability**: Easy to test each layer independently
3. **Maintainability**: Changes in one layer don't affect others
4. **Scalability**: Easy to add new features or modify existing ones
5. **Reusability**: Business logic can be reused across different interfaces

## Adding New Features

### Adding a New Endpoint

1. **Add route in router** (`app/routers/address.py`):
```python
@router.get("/custom")
def custom_endpoint(db: Session = Depends(get_db)):
    return AddressService.custom_method(db)
```

2. **Add business logic in service** (`app/services/address_service.py`):
```python
@staticmethod
def custom_method(db: Session):
    # Business logic here
    return crud_custom_method(db)
```

3. **Add CRUD operation** (`app/crud.py`):
```python
def custom_method(db: Session):
    # Database operation
    return result
```
