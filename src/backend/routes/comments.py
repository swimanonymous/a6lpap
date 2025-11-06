"""Comment CRUD endpoints."""
from flask import Blueprint, request, jsonify
from src.backend.models import Tasks, Comments
from src.backend.utils import (
    jsonify_comment, oid, parse_pagination, error_response
)


comments_bp = Blueprint('comments', __name__, url_prefix='/api')


@comments_bp.route('/tasks/<task_id>/comments', methods=['POST'])
def create_comment(task_id):
    """Create a comment for a task."""
    task_oid = oid(task_id)
    if not task_oid:
        return error_response("Invalid task ID", 400)
    
    # Verify task exists
    task = Tasks.find_by_id(task_oid)
    if not task:
        return error_response("Task not found", 404)
    
    data = request.get_json()
    if not data:
        return error_response("Request body is required", 400)
    
    body = data.get('body', '').strip()
    if not body:
        return error_response("Body is required and cannot be empty", 400)
    
    author = data.get('author', '').strip() or None
    
    comment = Comments.create(task_oid, body, author)
    return jsonify(jsonify_comment(comment)), 201


@comments_bp.route('/tasks/<task_id>/comments', methods=['GET'])
def list_comments(task_id):
    """List comments for a task with pagination."""
    task_oid = oid(task_id)
    if not task_oid:
        return error_response("Invalid task ID", 400)
    
    # Verify task exists
    task = Tasks.find_by_id(task_oid)
    if not task:
        return error_response("Task not found", 404)
    
    limit, offset, error = parse_pagination(request)
    if error:
        return error_response(error, 400)
    
    comments, total = Comments.find_by_task(task_oid, limit, offset)
    
    return jsonify({
        'comments': [jsonify_comment(c) for c in comments],
        'count': total,
        'limit': limit,
        'offset': offset
    }), 200


@comments_bp.route('/comments/<comment_id>', methods=['PATCH'])
def update_comment(comment_id):
    """Update a comment."""
    comment_oid = oid(comment_id)
    if not comment_oid:
        return error_response("Invalid comment ID", 400)
    
    data = request.get_json()
    if not data:
        return error_response("Request body is required", 400)
    
    updates = {}
    
    if 'body' in data:
        body = data['body'].strip()
        if not body:
            return error_response("Body cannot be empty", 400)
        updates['body'] = body
    
    if 'author' in data:
        updates['author'] = data['author'].strip() or None
    
    if not updates:
        return error_response("At least one field (body or author) is required", 400)
    
    comment = Comments.update(comment_oid, updates)
    if not comment:
        return error_response("Comment not found", 404)
    
    return jsonify(jsonify_comment(comment)), 200


@comments_bp.route('/comments/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """Delete a comment."""
    comment_oid = oid(comment_id)
    if not comment_oid:
        return error_response("Invalid comment ID", 400)
    
    deleted = Comments.delete(comment_oid)
    if not deleted:
        return error_response("Comment not found", 404)
    
    return '', 204