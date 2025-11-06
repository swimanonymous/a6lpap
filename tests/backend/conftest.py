"""Pytest fixtures for backend tests."""
import os
import random
import string
import pytest
from src.backend.app import create_app
from src.backend.db import get_client, close_db


@pytest.fixture(scope='session')
def test_db_name():
    """Generate unique test database name."""
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"better_software_test_{suffix}"


@pytest.fixture(scope='session')
def app(test_db_name):
    """Create Flask app for testing."""
    os.environ['DB_NAME'] = test_db_name
    os.environ['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    
    app = create_app()
    app.config['TESTING'] = True
    
    yield app
    
    # Cleanup: drop test database
    client = get_client()
    client.drop_database(test_db_name)
    close_db()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db(app, test_db_name):
    """Clean database before each test."""
    client = get_client()
    db = client[test_db_name]
    
    # Clear collections
    db.tasks.delete_many({})
    db.comments.delete_many({})
    
    yield
    
    # Cleanup after test
    db.tasks.delete_many({})
    db.comments.delete_many({})