# Trip API Examples

This directory contains example JSON payloads for testing the Trip CRUD operations.

## CREATE Trip Examples

### Full Example with All Fields
**File**: `example_trip_create.json`

```json
{
  "destination": "Paris, France",
  "start_date": "2024-07-15T08:00:00Z",
  "end_date": "2024-07-22T20:00:00Z",
  "coordinates": "48.8566,2.3522",
  "itinerary": "Day 1: Arrival and Eiffel Tower visit\n..."
}
```

### Minimal Required Fields Only
**File**: `example_trip_minimal.json`

```json
{
  "destination": "Tokyo, Japan",
  "start_date": "2024-09-01T09:00:00Z",
  "end_date": "2024-09-10T18:00:00Z"
}
```

### With Coordinates (No Itinerary)
**File**: `example_trip_coordinates.json`

```json
{
  "destination": "New York City, USA",
  "start_date": "2024-11-20T14:00:00Z",
  "end_date": "2024-11-27T12:00:00Z",
  "coordinates": "40.7128,-74.0060"
}
```

## GET Trip by ID Examples

### Fetch Trip with ID 1

```bash
curl -X GET http://127.0.0.1:5000/trips/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response** (200 OK):
```json
{
  "trip": {
    "id": 1,
    "user_id": 1,
    "destination": "Paris, France",
    "start_date": "2024-07-15T08:00:00",
    "end_date": "2024-07-22T20:00:00",
    "coordinates": "48.8566,2.3522",
    "itinerary": "Day 1: Arrival and Eiffel Tower visit\nDay 2: Louvre Museum and Seine River cruise\n...",
    "created_at": "2024-05-13T10:30:00",
    "updated_at": "2024-05-13T10:30:00"
  }
}
```

### Fetch Trip with ID 2

```bash
curl -X GET http://127.0.0.1:5000/trips/2 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response** (200 OK):
```json
{
  "trip": {
    "id": 2,
    "user_id": 1,
    "destination": "Tokyo, Japan",
    "start_date": "2024-09-01T09:00:00",
    "end_date": "2024-09-10T18:00:00",
    "coordinates": null,
    "itinerary": null,
    "created_at": "2024-05-13T11:00:00",
    "updated_at": "2024-05-13T11:00:00"
  }
}
```

### Error: Trip Not Found

```bash
curl -X GET http://127.0.0.1:5000/trips/999 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response** (404 Not Found):
```json
{
  "error": "Trip not found."
}
```

## How to Test

1. Start your Flask server:
   ```bash
   python app.py
   ```

2. Register/Login to get a JWT token

3. Use curl to test the CREATE endpoint:
   ```bash
   curl -X POST http://127.0.0.1:5000/trips \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d @example_trip_create.json
   ```

4. Use curl to test the GET endpoint:
   ```bash
   curl -X GET http://127.0.0.1:5000/trips/1 \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

## Field Requirements

- **destination** (required): String, non-empty
- **start_date** (required): ISO 8601 datetime string
- **end_date** (required): ISO 8601 datetime string, must be after start_date
- **coordinates** (optional): String, typically "lat,lng" format
- **itinerary** (optional): String, can contain multi-line text

## Expected Response

Success (201 Created):
```json
{
  "trip": {
    "id": 1,
    "user_id": 123,
    "destination": "Paris, France",
    "start_date": "2024-07-15T08:00:00",
    "end_date": "2024-07-22T20:00:00",
    "coordinates": "48.8566,2.3522",
    "itinerary": "Day 1: Arrival and Eiffel Tower visit...",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

## Error Responses

- **400 Bad Request**: Missing required fields, invalid dates, empty destination, end_date before start_date
- **401 Unauthorized**: Missing or invalid JWT token
- **404 Not Found**: User not found (shouldn't happen with valid token)