"""
==============================================
DATABASE.PY - Database Connection
==============================================

SQLite database connection and SQLAlchemy session management.
SQLite was chosen because:
- No installation required
- Single .db file
- Ideal for development stage
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file path — always created inside Backend/ directory
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(_BASE_DIR, 'espressolab.db')}"

# SQLAlchemy engine
# check_same_thread=False: allows FastAPI to use multiple threads
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Separate database session per request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that all model classes inherit from
Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session.

    FastAPI calls this function for each endpoint to obtain
    a database connection and closes it after the request is complete.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
