# PlanVenture API

A comprehensive REST API for trip planning and itinerary management, built with Flask and SQLAlchemy. PlanVenture allows users to create, manage, and organize their travel plans with automatic itinerary generation.

## 🚀 Features

- **User Authentication**: Secure JWT-based authentication system
- **Trip Management**: Full CRUD operations for trip planning
- **Automatic Itinerary Generation**: AI-powered itinerary templates
- **Geographic Coordinates**: Location-based trip planning
- **CORS Support**: Ready for React frontend integration
- **SQLite Database**: Lightweight, file-based database for development
- **Environment Configuration**: Flexible configuration via environment variables

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Trip Management](#trip-management)
- [Itinerary Generation](#itinerary-generation)
- [Configuration](#configuration)
- [Database](#database)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd planventure-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .sample.env .env
   # Edit .env with your configuration
   ```

5. **Initialize the database**
   ```bash
   python init_db.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## 📡 API Endpoints

### Base URL
```
http://localhost:5000
```

### Health Check Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /db-status` - Database connection status
- `GET /protected` - Protected route (requires authentication)

### Authentication Endpoints (`/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | User registration | No |
| POST | `/auth/login` | User login | No |
| POST | `/auth/refresh` | Refresh access token | Yes (refresh token) |

### Trip Management Endpoints (`/trips`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/trips` | Get all user trips | Yes |
| GET | `/trips/<id>` | Get specific trip | Yes |
| POST | `/trips` | Create new trip | Yes |
| PUT | `/trips/<id>` | Update trip | Yes |
| DELETE | `/trips/<id>` | Delete trip | Yes |

## 🔐 Authentication

PlanVenture uses JWT (JSON Web Tokens) for authentication. All protected endpoints require a valid access token in the `Authorization` header.

### Register User

```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

### Login

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com"
  }
}
```

### Using Access Tokens

Include the access token in the `Authorization` header:

```bash
curl -X GET http://localhost:5000/trips \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## ✈️ Trip Management

### Create Trip

```bash
curl -X POST http://localhost:5000/trips \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris, France",
    "start_date": "2024-07-15T08:00:00Z",
    "end_date": "2024-07-22T20:00:00Z",
    "coordinates": "48.8566,2.3522",
    "auto_generate_itinerary": true
  }'
```

**Required Fields:**
- `destination`: Trip destination (string)
- `start_date`: ISO 8601 formatted start date (string)
- `end_date`: ISO 8601 formatted end date (string)

**Optional Fields:**
- `coordinates`: Geographic coordinates as "lat,lng" (string)
- `itinerary`: Custom itinerary text (string)
- `auto_generate_itinerary`: Generate automatic itinerary (boolean)

### Get Trips

```bash
curl -X GET http://localhost:5000/trips \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "trips": [
    {
      "id": 1,
      "user_id": 1,
      "destination": "Paris, France",
      "start_date": "2024-07-15T08:00:00",
      "end_date": "2024-07-22T20:00:00",
      "coordinates": "48.8566,2.3522",
      "itinerary": "# Paris, France Itinerary\n...",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ],
  "count": 1
}
```

### Update Trip

```bash
curl -X PUT http://localhost:5000/trips/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris & Versailles, France",
    "coordinates": "48.8566,2.3522"
  }'
```

### Delete Trip

```bash
curl -X DELETE http://localhost:5000/trips/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📝 Itinerary Generation

PlanVenture provides automatic itinerary generation with two template functions:

### Auto-Generated Itineraries

When creating a trip with `"auto_generate_itinerary": true`, the API generates a detailed markdown itinerary based on:

- Trip duration (calculated from start/end dates)
- Destination name
- Daily structure with Morning/Afternoon/Evening sections

**Example Generated Itinerary:**
```markdown
# Paris, France Itinerary

**Trip Duration:** 7 days
**Dates:** July 15, 2024 - July 22, 2024

## Day 1 - July 15
### Morning
- Activity or location

### Afternoon
- Activity or location

### Evening
- Activity or location

## Notes
- Add any special notes or important information
- Include restaurant recommendations
- Mark unmissable attractions
```

### Custom Itineraries

You can also provide custom itinerary content:

```json
{
  "destination": "Tokyo, Japan",
  "start_date": "2024-09-01T09:00:00Z",
  "end_date": "2024-09-10T18:00:00Z",
  "itinerary": "# Tokyo Trip\n\n## Day 1\n- Visit Senso-ji Temple\n- Explore Asakusa district\n\n## Day 2\n- Mount Fuji day trip\n- Hakone onsen"
}
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=1
PORT=5000

# Database
DATABASE_URL=sqlite:///planventure.db

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_TOKEN_EXPIRES=3600

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `change-this-secret` | Flask secret key for sessions |
| `JWT_SECRET_KEY` | Same as SECRET_KEY | JWT token signing key |
| `JWT_ACCESS_TOKEN_EXPIRES` | `3600` | Access token expiration in seconds |
| `DATABASE_URL` | `sqlite:///planventure.db` | Database connection string |
| `CORS_ORIGINS` | `http://localhost:3000,http://127.0.0.1:3000` | Allowed CORS origins |
| `FLASK_DEBUG` | `1` | Enable/disable debug mode |
| `PORT` | `5000` | Server port |

## 🗄️ Database

### Schema

#### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
```

#### Trips Table
```sql
CREATE TABLE trips (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    destination VARCHAR(255) NOT NULL,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    coordinates VARCHAR(255),
    itinerary TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Database Initialization

Run the database initialization script:

```bash
python init_db.py
```

This creates all tables and sets up the database schema.

## 🧪 Testing

### Run API Tests

```bash
python test_trips_api.py
```

### Manual Testing with cURL

Use the provided example files for testing:

```bash
# Register a user
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d @example_user_register.json

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d @example_user_login.json

# Create trip (replace TOKEN with actual JWT)
curl -X POST http://localhost:5000/trips \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d @example_trip_create.json
```

### Example Files

- `example_trip_create.json` - Full trip creation example
- `example_trip_minimal.json` - Minimal required fields
- `example_trip_coordinates.json` - With geographic coordinates
- `example_trip_auto_itinerary.json` - Auto-generated itinerary

## 🚀 Deployment

### Production Considerations

1. **Change Secret Keys**: Use strong, unique secret keys in production
2. **Database**: Use PostgreSQL or MySQL instead of SQLite
3. **HTTPS**: Enable SSL/TLS in production
4. **Environment Variables**: Set all required environment variables
5. **CORS Origins**: Configure allowed origins for your frontend domain

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python init_db.py

EXPOSE 5000
CMD ["python", "app.py"]
```

### Environment Setup for Production

```env
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-production-jwt-secret
DATABASE_URL=postgresql://user:password@localhost/planventure
CORS_ORIGINS=https://your-frontend-domain.com
FLASK_DEBUG=0
PORT=8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest

# Run linting
flake8 .

# Format code
black .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, email support@planventure.com or create an issue in the repository.

## 🙏 Acknowledgments

- Flask framework for the web application
- SQLAlchemy for database ORM
- Flask-JWT-Extended for authentication
- Flask-CORS for cross-origin support

---

**PlanVenture API** - Making trip planning effortless! 🌍✈️