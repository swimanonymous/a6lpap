"""Data models and database operations."""
from datetime import datetime
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from src.backend.db import get_db


class Tasks:
    """Task model operations."""
    
    @staticmethod
    def create(title, description=None, status='todo'):
        """Create a new task."""
        db = get_db()
        now = datetime.utcnow()
        task = {
            'title': title,
            'description': description,
            'status': status,
            'created_at': now,
            'updated_at': now
        }
        result = db.tasks.insert_one(task)
        task['_id'] = result.inserted_id
        return task
    
    @staticmethod
    def find_by_id(task_id):
        """Find task by ID."""
        db = get_db()
        return db.tasks.find_one({'_id': ObjectId(task_id)})
    
    @staticmethod
    def find_all():
        """Find all tasks."""
        db = get_db()
        return list(db.tasks.find().sort('created_at', -1))
    
    @staticmethod
    def update(task_id, updates):
        """Update a task."""
        db = get_db()
        updates['updated_at'] = datetime.utcnow()
        result = db.tasks.update_one(
            {'_id': ObjectId(task_id)},
            {'$set': updates}
        )
        if result.matched_count == 0:
            return None
        return Tasks.find_by_id(task_id)
    
    @staticmethod
    def delete(task_id):
        """Delete a task and its comments."""
        db = get_db()
        # Delete associated comments first
        db.comments.delete_many({'task_id': ObjectId(task_id)})
        # Delete task
        result = db.tasks.delete_one({'_id': ObjectId(task_id)})
        return result.deleted_count > 0


class Comments:
    """Comment model operations."""
    
    @staticmethod
    def create(task_id, body, author=None):
        """Create a new comment."""
        db = get_db()
        now = datetime.utcnow()
        comment = {
            'task_id': ObjectId(task_id),
            'body': body,
            'author': author,
            'created_at': now,
            'updated_at': now
        }
        result = db.comments.insert_one(comment)
        comment['_id'] = result.inserted_id
        return comment
    
    @staticmethod
    def find_by_id(comment_id):
        """Find comment by ID."""
        db = get_db()
        return db.comments.find_one({'_id': ObjectId(comment_id)})
    
    @staticmethod
    def find_by_task(task_id, limit=20, offset=0):
        """Find comments for a task with pagination."""
        db = get_db()
        comments = list(
            db.comments.find({'task_id': ObjectId(task_id)})
            .sort('created_at', -1)
            .skip(offset)
            .limit(limit)
        )
        total = db.comments.count_documents({'task_id': ObjectId(task_id)})
        return comments, total
    
    @staticmethod
    def update(comment_id, updates):
        """Update a comment."""
        db = get_db()
        updates['updated_at'] = datetime.utcnow()
        result = db.comments.update_one(
            {'_id': ObjectId(comment_id)},
            {'$set': updates}
        )
        if result.matched_count == 0:
            return None
        return Comments.find_by_id(comment_id)
    
    @staticmethod
    def delete(comment_id):
        """Delete a comment."""
        db = get_db()
        result = db.comments.delete_one({'_id': ObjectId(comment_id)})
        return result.deleted_count > 0