#!/usr/bin/env python3
"""Create database tables directly"""

from app.models.simple import Base as SimpleBase
from app.auth.models import Base as AuthBase
from app.database import engine

if __name__ == "__main__":
    print("Creating all tables...")
    # Create auth tables first
    AuthBase.metadata.create_all(bind=engine)
    # Then create app tables
    SimpleBase.metadata.create_all(bind=engine)
    print("Tables created successfully!")