# Social Hub API

Social Hub API is a backend application for a social platform, built with **FastAPI**, demonstrating a modern and production-oriented approach to REST API development.

---

## Key Features

- User registration and login
- Authentication via **access/refresh tokens**
- Token storage in **HttpOnly cookies**
- **Refresh token rotation** with revocation capability
- Logout with refresh token revocation
- Sending **welcome email** after registration (background task)
- Asynchronous database operations (SQLAlchemy + AsyncSession)
- Clear separation of responsibilities with folders inside `app/`:
  - `app/api/` - Routers (HTTP level)
  - `app/services/` - Business logic
  - `app/repositories/` - Database operations

---

## Technologies

- **Python 3.12**
- **FastAPI**
- **SQLAlchemy (async)**
- **PostgreSQL**
- **Alembic** (migrations)
- **JWT** (access tokens)
- **HttpOnly Cookies**
- **Pytest** (integration tests)

---

## Authentication

- **Access token** — short-lived JWT used for request authorization
- **Refresh token** — random token stored in the database in hashed form
- **Refresh token rotation** implemented
- Refresh and access tokens stored in **HttpOnly cookies**

---

## Project Structure
```
├── app/ # Main application package
│   ├── api/ # API routers
│   │    └── v1/
│   │        ├── auth.py
│   │        └── ...
│   ├── core/ # Configuration, security
│   ├── db/ # Database session management
│   ├── exceptions/ # Custom exceptions
│   ├── middleware/ # Custom middleware
│   ├── models/ # SQLAlchemy models
│   ├── repositories/ # Data access layer
│   │     ├── user.py
│   │     ├── token.py
│   │     └── ...
│   ├── schemas/ # Pydantic schemas
│   ├── services/ # Business logic layer
│   │     ├── auth.py
│   │     ├── email.py
│   │     └── ...
│   ├── main.py # FastAPI app
│   ├── dependencies.py # FastAPI dependencies
│   └── exception_handler.py # Global exception handlers
├── tests/ # Integration tests
│     ├── conftest.py
│     ├── test_auth.py
│     └── ...
├── alembic.ini # Alembic configuration
├── .env
├── .env.example
├── .docker-compose.yml # Docker Compose
├── Dockerfile
└── requirements.txt # Python packages
```

---

## Tests

- Integration tests for auth endpoints (`tests/`)
- Separate test database
- Dependency overrides via `Depends`
- pytest fixtures in `tests/conftest.py`

---

## Quick Start

### 1. Clone & Setup
```
git clone <your-repo>
cp .env.example .env
```

### 2. Docker (Recommended)
```
# Start services
.docker-compose up --build

# Apply migrations
.docker-compose exec web alembic upgrade head

# Access API: http://localhost:8000
# Access Docs: http://localhost:8000/docs
```

### 3. Local Development
```
# Install dependencies
pip install -r requirements.txt

# Apply migrations
alembic upgrade head

# Run server
uvicorn app.main:app --reload
```

---

## Environment Variables

Copy .env.example to .env and update:
```
# JWT Settings
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/socialhub
TEST_DATABASE_URL=sqlite+aiosqlite:///./test.db

# Email (for welcome emails)
ADMIN_GMAIL=your_email@gmail.com
APP_PASSWORD=your_16_digit_app_password
```

---

## Docker Services

.docker-compose.yml includes:

| Service | Port | Description                          |
| ------- | ---- | ------------------------------------ |
| web     | 8000 | FastAPI app with hot reload          |
| db      | 5432 | PostgreSQL 16 with persistent volume |

```
# Stop services
.docker-compose down

# Reset database
.docker-compose down -v
```

---

## API Documentation

Swagger UI: http://localhost:8000/api/docs

ReDoc: http://localhost:8000/redoc

---

## Endpoints:

### Authentication
```
POST /auth/register     # User registration
POST /auth/login        # User login
POST /auth/refresh      # Token refresh
POST /auth/logout       # User logout
```

### User
```
GET  /users/me          # Get current user
GET  /users/{user_id}   # Get user by ID
DELETE /users/me        # Delete current account
```

### Post
```
GET    /posts           # Get all posts (paginated)
GET    /posts/{id}      # Get specific post
POST   /posts           # Create new post
DELETE /posts/{id}      # Delete own post
```

### Comment & Like
```
GET    /posts/{id}/comments  # Get post comments
POST   /posts/{id}/comments  # Add comment
GET    /comments/delete      # Delete comment
POST   /posts/{id}/like      # Like a post
DELETE /posts/{id}/like      # Remove like
```

### Friendship
```
GET    /friends              # List all friends
GET    /friends/requests     # List friend requests
POST   /friends/{user_id}    # Send friend request
POST   /friends/{id}/accept  # Accept request
POST   /friends/{id}/reject  # Reject request
DELETE /friends/{user_id}    # Remove friend
```

---

## Project Goals
Social Hub API demonstrates enterprise-grade architecture:

- Clean separation: api/, services/, repositories/
- Dedicated db/, middleware/, core/ modules
- Production Docker setup (.docker-compose.yml)
- Professional testing strategy (tests/)
- Dotfile conventions for config

Project ready for extension and can serve as the basis for a full-fledged social platform.

---
