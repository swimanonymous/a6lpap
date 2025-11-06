"""MongoDB database connection and helpers."""
import os
from pymongo import MongoClient, DESCENDING
from pymongo.errors import ConnectionFailure


_client = None
_db = None


def get_client():
    """Get MongoDB client singleton."""
    global _client
    if _client is None:
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
        _client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        try:
            # Verify connection
            _client.admin.command('ping')
        except ConnectionFailure as e:
            raise ConnectionFailure(f"Cannot connect to MongoDB: {e}")
    return _client


def get_db():
    """Get database instance."""
    global _db
    if _db is None:
        client = get_client()
        db_name = os.getenv('DB_NAME', 'better_software_dev')
        _db = client[db_name]
        _ensure_indexes()
    return _db


def _ensure_indexes():
    """Create necessary indexes."""
    db = _db
    # Index on (task_id, -created_at) for efficient comment queries
    db.comments.create_index([('task_id', 1), ('created_at', DESCENDING)])


def close_db():
    """Close database connection."""
    global _client, _db
    if _client is not None:
        _client.close()
        _client = None
        _db = None