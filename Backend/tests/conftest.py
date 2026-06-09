import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# OAuth / JWT must be configured before routers import env at module load time
os.environ.setdefault("GOOGLE_CLIENT_ID", "test-google-client-id.apps.googleusercontent.com")
os.environ.setdefault("GOOGLE_CLIENT_SECRET", "test-google-client-secret")
os.environ.setdefault("JWT_SECRET", "test-jwt-secret-for-ci")

from main import app
from database import Base, get_db

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Create the tables in the test database
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop the tables after the test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Clean up override
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def mock_session_local(monkeypatch):
    """
    Ensure the queue consumer and the database module use the in-memory SQLite DB
    used for testing instead of writing to the production sqlite file.
    """
    import queue_consumer
    import database
    monkeypatch.setattr(queue_consumer, "SessionLocal", TestingSessionLocal)
    monkeypatch.setattr(database, "SessionLocal", TestingSessionLocal)


@pytest.fixture(autouse=True)
def sync_rabbitmq(monkeypatch):
    """
    Automatically intercept queue publishing in tests and route messages
    directly to the consumer's callback synchronously.
    This simulates asynchronous processing while keeping tests synchronous and simple.
    """
    import queue_service
    import queue_consumer
    from unittest.mock import MagicMock
    import json
    
    def mock_publish(message: dict):
        body = json.dumps(message).encode("utf-8")
        ch = MagicMock()
        method = MagicMock()
        method.delivery_tag = 1
        properties = MagicMock()
        
        # Disable sleep in callback to speed up tests
        import time
        orig_sleep = time.sleep
        time.sleep = lambda s: None
        try:
            queue_consumer.callback(ch, method, properties, body)
        finally:
            time.sleep = orig_sleep
        return True
        
    monkeypatch.setattr(queue_service.queue_service, "publish_message", mock_publish)

