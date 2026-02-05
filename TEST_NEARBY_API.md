# Testing the Nearby Addresses API

## Endpoint
**GET** `/api/v1/addresses/nearby`

## Query Parameters
- `latitude` (required): Center point latitude
- `longitude` (required): Center point longitude  
- `distance_km` (required): Search radius in kilometers (must be > 0)

## Step-by-Step Testing Guide

### Step 1: Create Some Test Addresses

First, create a few addresses to search from:

```bash
# Create address 1 - Near the center point
curl -X POST "http://127.0.0.1:8000/api/v1/addresses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nearby Location 1",
    "latitude": "22.705",
    "longitude": "75.844"
  }'

# Create address 2 - Also nearby
curl -X POST "http://127.0.0.1:8000/api/v1/addresses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nearby Location 2",
    "latitude": "22.702",
    "longitude": "75.838"
  }'

# Create address 3 - Far away
curl -X POST "http://127.0.0.1:8000/api/v1/addresses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Far Location",
    "latitude": "23.500",
    "longitude": "76.500"
  }'
```

### Step 2: Test the Nearby Endpoint

#### Example 1: Find addresses within 5km

```bash
curl "http://127.0.0.1:8000/api/v1/addresses/nearby?latitude=22.700&longitude=75.840&distance_km=5"
```

**Expected Response:**
```json
[
  {
    "id": 1,
    "name": "Nearby Location 1",
    "latitude": "22.705",
    "longitude": "75.844"
  },
  {
    "id": 2,
    "name": "Nearby Location 2",
    "latitude": "22.702",
    "longitude": "75.838"
  }
]
```

#### Example 2: Find addresses within 1km (should find fewer)

```bash
curl "http://127.0.0.1:8000/api/v1/addresses/nearby?latitude=22.700&longitude=75.840&distance_km=1"
```

#### Example 3: Find addresses within 100km (should find all)

```bash
curl "http://127.0.0.1:8000/api/v1/addresses/nearby?latitude=22.700&longitude=75.840&distance_km=100"
```

#### Example 4: Using coordinate format with degrees

```bash
curl "http://127.0.0.1:8000/api/v1/addresses/nearby?latitude=22.705435°%20N&longitude=75.84361°%20E&distance_km=5"
```

Or with URL encoding:
```bash
curl "http://127.0.0.1:8000/api/v1/addresses/nearby?latitude=22.705435%C2%B0%20N&longitude=75.84361%C2%B0%20E&distance_km=5"
```

### Step 3: Test Error Cases

#### Invalid distance (should return 400)

```bash
curl "http://127.0.0.1:8000/api/v1/addresses/nearby?latitude=22.700&longitude=75.840&distance_km=0"
```

**Expected Response:**
```json
{
  "detail": "distance_km must be greater than 0"
}
```

#### Negative distance (should return 400)

```bash
curl "http://127.0.0.1:8000/api/v1/addresses/nearby?latitude=22.700&longitude=75.840&distance_km=-5"
```

## Using Python requests

```python
import requests

# Base URL
base_url = "http://127.0.0.1:8000/api/v1"

# Test nearby addresses
response = requests.get(
    f"{base_url}/addresses/nearby",
    params={
        "latitude": 22.700,
        "longitude": 75.840,
        "distance_km": 5
    }
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
```

## Using JavaScript/Fetch

```javascript
// Test nearby addresses
const response = await fetch(
  'http://127.0.0.1:8000/api/v1/addresses/nearby?latitude=22.700&longitude=75.840&distance_km=5'
);

const data = await response.json();
console.log(data);
```

## Using Postman

1. Create a new GET request
2. URL: `http://127.0.0.1:8000/api/v1/addresses/nearby`
3. Go to "Params" tab and add:
   - Key: `latitude`, Value: `22.700`
   - Key: `longitude`, Value: `75.840`
   - Key: `distance_km`, Value: `5`
4. Click "Send"

## Expected Behavior

- ✅ Returns addresses sorted by distance (closest first)
- ✅ Only includes addresses within the specified radius
- ✅ Returns empty array `[]` if no addresses found
- ✅ Handles both string and numeric coordinate formats
- ✅ Validates that distance_km > 0
- ✅ Returns 400 error for invalid coordinates

## Quick Test Script

Save this as `test_nearby.sh`:

```bash
#!/bin/bash

BASE_URL="http://127.0.0.1:8000/api/v1"

echo "Creating test addresses..."
curl -X POST "$BASE_URL/addresses" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Location 1", "latitude": "22.705", "longitude": "75.844"}' \
  -s | jq

echo -e "\nSearching nearby addresses..."
curl "$BASE_URL/addresses/nearby?latitude=22.700&longitude=75.840&distance_km=5" \
  -s | jq
```

Make it executable and run:
```bash
chmod +x test_nearby.sh
./test_nearby.sh
```
