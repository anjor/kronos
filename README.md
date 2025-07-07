# Kronos Calendar Management System

A multi-calendar management system for freelancers that syncs events from Google Calendar, Microsoft Calendar, and Cal.com, detects conflicts, and provides unified availability management.

## Features

- **Multi-Calendar Sync**: Connect and sync with Google Calendar, Microsoft Calendar, and Cal.com
- **Conflict Detection**: Automatically detect scheduling conflicts across all calendars
- **Availability Management**: Calculate and export availability for seamless booking
- **Client Management**: Organize events by clients and projects
- **Real-time Updates**: Webhook support for live calendar synchronization
- **RESTful API**: Complete API for integration with other tools

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: Next.js, TypeScript, Tailwind CSS (in development)
- **Authentication**: JWT with bcrypt
- **Background Jobs**: Celery, Redis (planned)
- **Deployment**: Docker, nginx
- **Calendar APIs**: Google Calendar, Microsoft Graph (planned)

## Quick Start

### Development Setup

1. **Clone and setup environment:**
   ```bash
   git clone https://github.com/anjor/kronos.git
   cd kronos
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start backend services:**
   ```bash
   docker compose up -d  # PostgreSQL + Redis
   uv sync               # Install Python dependencies
   uv run python create_tables.py  # Create database tables
   uv run uvicorn app.main:app --reload  # Start API server
   ```

3. **Start frontend (in development):**
   ```bash
   cd frontend
   npm install
   npm run dev  # Starts on http://localhost:3000
   ```

### Production Deployment

1. **Configure environment:**
   ```bash
   cp .env.example .env
   # Set production values for SECRET_KEY, etc.
   ```

2. **Deploy with Docker:**
   ```bash
   ./deploy.sh  # Coming soon
   ```

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

### Development Commands

```bash
# Activate virtual environment
uv shell

# Run development server
uv run uvicorn app.main:app --reload

# Run database migrations
uv run alembic upgrade head

# Create new migration
uv run alembic revision --autogenerate -m "migration message"

# Run Celery worker
uv run celery -A app.tasks worker --loglevel=info

# Run tests
uv run pytest

# Database admin (optional)
# Access at http://localhost:8080
docker-compose up -d adminer
```

## Configuration

### Environment Variables

Key configuration options in `.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/kronos

# OAuth Credentials
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
MICROSOFT_CLIENT_ID=your-microsoft-client-id
MICROSOFT_CLIENT_SECRET=your-microsoft-client-secret
CALDOTCOM_API_KEY=your-caldotcom-api-key

# Security
SECRET_KEY=your-secret-key-change-in-production
```

### OAuth Setup

1. **Google Calendar**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project and enable Calendar API
   - Create OAuth 2.0 credentials
   - Add redirect URI: `http://localhost:8000/api/auth/callback/google`

2. **Microsoft Calendar**:
   - Go to [Azure App Registration](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps)
   - Register a new application
   - Add redirect URI: `http://localhost:8000/api/auth/callback/microsoft`
   - Grant Calendar permissions

3. **Cal.com**:
   - Get API key from your Cal.com account settings

## API Documentation

### Authentication Endpoints

```http
POST /api/auth/register        # User registration
POST /api/auth/login           # User login (JWT)
GET  /api/auth/connect/{provider}  # Start OAuth flow
GET  /api/auth/callback/{provider} # OAuth callback
POST /api/auth/disconnect/{provider} # Remove calendar connection
```

### Calendar Management

```http
GET    /api/calendars          # Get connected calendars
POST   /api/calendars/{id}/sync # Manual sync trigger
PATCH  /api/calendars/{id}     # Update calendar settings
DELETE /api/calendars/{id}     # Disconnect calendar
```

### Event Management

```http
GET   /api/events              # Get events (with filters)
GET   /api/events/{id}         # Get specific event
PATCH /api/events/{id}/client  # Assign event to client
```

### Availability & Conflicts

```http
GET  /api/availability         # Get available time slots
POST /api/availability/rules   # Set availability preferences
GET  /api/conflicts            # Get detected conflicts
POST /api/conflicts/{id}/resolve # Mark conflict as resolved
```

## Project Structure

```
kronos/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connection
│   ├── models/                # SQLAlchemy models
│   │   ├── user.py
│   │   ├── calendar.py
│   │   ├── event.py
│   │   ├── client.py
│   │   └── conflict.py
│   ├── schemas/               # Pydantic schemas
│   ├── api/                   # API route handlers
│   ├── services/              # Business logic
│   ├── tasks/                 # Celery background tasks
│   └── utils/                 # Utility functions
├── migrations/                # Alembic database migrations
├── tests/                     # Test files
├── docker-compose.yml         # Development services
├── pyproject.toml            # Project dependencies
└── .env.example              # Environment template
```

## Development Workflow

### Adding New Features

1. Create database models in `app/models/`
2. Generate migration: `uv run alembic revision --autogenerate -m "add feature"`
3. Create Pydantic schemas in `app/schemas/`
4. Implement business logic in `app/services/`
5. Add API routes in `app/api/`
6. Write tests in `tests/`

### Database Management

```bash
# Create new migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1

# View migration history
uv run alembic history
```

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app

# Run specific test file
uv run pytest tests/test_auth.py
```

## Deployment

### Production Setup

1. Set `ENVIRONMENT=production` and `DEBUG=false`
2. Use strong `SECRET_KEY`
3. Configure production database URL
4. Set up reverse proxy (nginx)
5. Use process manager (systemd, supervisor)

### Docker Production

```bash
# Build production image
docker build -t kronos .

# Run with environment variables
docker run -p 8000:8000 --env-file .env kronos
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Check the API documentation at `/docs`
- Review the configuration in `.env.example`