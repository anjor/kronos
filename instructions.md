# Calendar Management System - Build Instructions

## Project Overview
Build a multi-calendar management system for freelancers using Python/FastAPI backend. The system should sync events from Google Calendar, Microsoft Calendar, and Cal.com, detect conflicts, and provide unified availability management.

## Tech Stack
- **Backend**: Python 3.11+ with FastAPI
- **Package Management**: uv for fast dependency management
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Queue System**: Celery with Redis for background tasks
- **Authentication**: OAuth 2.0 for calendar providers
- **API Client Libraries**: 
  - `google-api-python-client` for Google Calendar
  - `msal` for Microsoft Graph API
  - `requests` for Cal.com API

## Project Structure
```
calendar_manager/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py              # Configuration and environment variables
│   ├── database.py            # Database connection and session management
│   ├── models/                # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── calendar.py
│   │   ├── event.py
│   │   ├── client.py
│   │   └── conflict.py
│   ├── schemas/               # Pydantic schemas for API
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── calendar.py
│   │   ├── event.py
│   │   └── auth.py
│   ├── api/                   # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py           # OAuth and authentication routes
│   │   ├── calendars.py      # Calendar management routes
│   │   ├── events.py         # Event CRUD routes
│   │   ├── conflicts.py      # Conflict detection routes
│   │   └── availability.py   # Availability calculation routes
│   ├── services/             # Business logic layer
│   │   ├── __init__.py
│   │   ├── oauth_service.py  # OAuth flow handling
│   │   ├── google_service.py # Google Calendar integration
│   │   ├── microsoft_service.py # Microsoft Graph integration
│   │   ├── caldotcom_service.py # Cal.com integration
│   │   ├── sync_service.py   # Calendar sync orchestration
│   │   ├── conflict_service.py # Conflict detection logic
│   │   └── availability_service.py # Availability calculation
│   ├── tasks/                # Celery background tasks
│   │   ├── __init__.py
│   │   ├── sync_tasks.py     # Calendar sync jobs
│   │   └── conflict_tasks.py # Conflict detection jobs
│   └── utils/
│       ├── __init__.py
│       ├── auth.py           # JWT and authentication utilities
│       ├── timezone.py       # Timezone handling utilities
│       └── validators.py     # Custom validation functions
├── migrations/               # Alembic database migrations
├── tests/
├── pyproject.toml           # uv project configuration and dependencies
├── uv.lock                  # uv lockfile for reproducible builds
├── docker-compose.yml        # For local development with PostgreSQL and Redis
└── .env.example
```

## Database Schema Implementation

### Step 1: Create SQLAlchemy Models
Create the following models based on the provided schema:

**app/models/user.py**:
- User model with id, email, name, timezone
- Relationship to calendars and clients

**app/models/calendar.py**:
- Calendar model with provider enum (google, microsoft, caldotcom)
- OAuth token storage
- Sync job tracking

**app/models/event.py**:
- Event model with full calendar event details
- JSONB field for attendees
- Relationship to conflicts and clients

**app/models/client.py**:
- Client model for project/client tracking
- Relationship to events through event_clients table

**app/models/conflict.py**:
- Conflict detection results
- Severity levels and resolution tracking

### Step 2: Database Configuration
- Set up Alembic for migrations
- Configure PostgreSQL connection with connection pooling
- Add indexes for performance (events by time range, user lookups)

## API Implementation

### Step 3: Core API Routes

**Authentication Routes (/api/auth/)**:
```python
POST /api/auth/register        # User registration
POST /api/auth/login           # User login (JWT)
GET /api/auth/connect/{provider}  # Start OAuth flow
GET /api/auth/callback/{provider} # OAuth callback handler
POST /api/auth/disconnect/{provider} # Remove calendar connection
```

**Calendar Routes (/api/calendars/)**:
```python
GET /api/calendars             # Get user's connected calendars
POST /api/calendars/{id}/sync  # Manual sync trigger
PATCH /api/calendars/{id}      # Update calendar settings
DELETE /api/calendars/{id}     # Disconnect calendar
```

**Event Routes (/api/events/)**:
```python
GET /api/events                # Get events (with date range filtering)
GET /api/events/{id}           # Get specific event
PATCH /api/events/{id}/client  # Assign event to client
```

**Availability Routes (/api/availability/)**:
```python
GET /api/availability          # Get available time slots
POST /api/availability/rules   # Set availability preferences
GET /api/availability/export   # Export for Cal.com integration
```

**Conflict Routes (/api/conflicts/)**:
```python
GET /api/conflicts             # Get detected conflicts
POST /api/conflicts/{id}/resolve # Mark conflict as resolved
```

## Service Layer Implementation

### Step 4: OAuth Service
- Implement OAuth 2.0 flows for Google, Microsoft, Cal.com
- Token refresh logic
- Secure token storage with encryption

### Step 5: Calendar Integration Services

**Google Calendar Service**:
- Use `google-api-python-client`
- Implement webhook subscriptions for real-time updates
- Handle rate limiting and pagination
- Support multiple Google calendars per user

**Microsoft Graph Service**:
- Use `msal` for authentication
- Implement webhook subscriptions
- Handle Outlook calendar sync
- Support both personal and business accounts

**Cal.com Service**:
- REST API integration for booking events
- Webhook handling for new bookings
- Availability export to Cal.com

### Step 6: Sync Service
- Orchestrate syncing across all connected calendars
- Implement incremental sync (only changed events)
- Handle sync conflicts and errors
- Queue management for large sync jobs

### Step 7: Conflict Detection Service
- Real-time conflict detection when events are added/updated
- Support different conflict types:
  - Direct time overlaps
  - Back-to-back meetings without buffer time
  - Travel time conflicts (future enhancement)
- Configurable conflict sensitivity

### Step 8: Availability Calculation Service
- Calculate free time slots based on all calendars
- Respect user availability rules (working hours, days off)
- Handle timezone conversions
- Generate availability for Cal.com integration

## Background Tasks Implementation

### Step 9: Celery Task Setup
- Configure Celery with Redis broker
- Implement periodic sync tasks
- Error handling and retry logic
- Task monitoring and logging

**Key Tasks**:
- Periodic calendar sync (every 15 minutes)
- Conflict detection after event changes
- Token refresh before expiration
- Cleanup old sync jobs and resolved conflicts

## Configuration and Environment

### Step 10: Environment Setup
Create comprehensive configuration for:
- Database URL
- Redis URL
- OAuth credentials for each provider:
  - Google: CLIENT_ID, CLIENT_SECRET
  - Microsoft: CLIENT_ID, CLIENT_SECRET, TENANT_ID
  - Cal.com: API_KEY
- JWT secret key
- Frontend URL for OAuth redirects

## Testing Strategy

### Step 11: Test Implementation
- Unit tests for each service
- Integration tests for OAuth flows
- API endpoint tests
- Mock external calendar APIs for testing
- Database fixture setup for tests

## Development Workflow

### Step 12: Local Development Setup

**Project Initialization**:
```bash
# Initialize new uv project
uv init calendar_manager
cd calendar_manager

# Add dependencies
uv add fastapi uvicorn sqlalchemy psycopg2-binary alembic
uv add celery redis python-multipart python-jose[cryptography]
uv add google-api-python-client msal requests
uv add pytest pytest-asyncio httpx --dev

# Create virtual environment and install dependencies
uv sync
```

**Development Commands**:
```bash
# Activate virtual environment
source .venv/bin/activate  # or uv shell

# Run development server
uv run uvicorn app.main:app --reload

# Run database migrations
uv run alembic upgrade head

# Run Celery worker
uv run celery -A app.tasks worker --loglevel=info

# Run tests
uv run pytest
```

- Docker Compose for PostgreSQL and Redis
- Environment variable management
- Database migration commands
- Celery worker startup

## API Documentation

### Step 13: Documentation
- FastAPI automatic OpenAPI documentation
- Comprehensive endpoint descriptions
- Example requests/responses
- Authentication flow documentation

## Specific Implementation Notes

1. **Timezone Handling**: Use `pytz` library and store all times in UTC
2. **Rate Limiting**: Implement rate limiting for external API calls
3. **Error Handling**: Comprehensive error handling with proper HTTP status codes
4. **Logging**: Structured logging for debugging and monitoring
5. **Security**: Input validation, SQL injection prevention, secure token storage
6. **Performance**: Database query optimization, connection pooling, caching

## MVP Feature Priority
1. User registration and OAuth setup
2. Google Calendar integration (most common)
3. Basic event sync and display
4. Simple conflict detection
5. Availability calculation
6. Microsoft Calendar integration
7. Cal.com integration
8. Advanced conflict resolution
9. Client/project management features

## Future Enhancements
- Team calendar support
- Advanced scheduling rules
- Analytics dashboard
- Mobile app API support
- Webhook API for third-party integrations

Start with the database models and basic FastAPI setup, then implement OAuth flows for Google Calendar first as the foundation.
