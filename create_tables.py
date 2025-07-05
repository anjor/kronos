#!/usr/bin/env python3
"""Create database tables directly"""

from app.models.simple import Base
from app.database import engine

if __name__ == "__main__":
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")