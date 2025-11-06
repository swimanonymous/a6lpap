"""Utility functions for serialization, validation, and error handling."""
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId


def to_iso(dt):
    """Convert datetime to ISO 8601 string."""
    if dt is None:
        return None
    if isinstance(dt, datetime):
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    return dt


def oid(value):
    """Parse and validate ObjectId."""
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        return None


def jsonify_task(task):
    """Convert task document to JSON-serializable dict."""
    if task is None:
        return None
    return {
        '_id': str(task['_id']),
        'title': task['title'],
        'description': task.get('description'),
        'status': task['status'],
        'created_at': to_iso(task['created_at']),
        'updated_at': to_iso(task['updated_at'])
    }


def jsonify_comment(comment):
    """Convert comment document to JSON-serializable dict."""
    if comment is None:
        return None
    return {
        '_id': str(comment['_id']),
        'task_id': str(comment['task_id']),
        'body': comment['body'],
        'author': comment.get('author'),
        'created_at': to_iso(comment['created_at']),
        'updated_at': to_iso(comment['updated_at'])
    }


def parse_pagination(request):
    """Parse and validate pagination parameters."""
    try:
        limit = int(request.args.get('limit', 20))
        offset = int(request.args.get('offset', 0))
    except ValueError:
        return None, None, "Invalid pagination parameters"
    
    if limit < 1:
        return None, None, "Limit must be at least 1"
    if limit > 100:
        limit = 100
    if offset < 0:
        return None, None, "Offset must be non-negative"
    
    return limit, offset, None


def error_response(message, status_code=400):
    """Create consistent error response."""
    return {'error': message}, status_code