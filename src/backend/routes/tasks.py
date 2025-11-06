"""Task CRUD endpoints."""
from flask import Blueprint, request, jsonify
from bson.errors import InvalidId
from src.backend.models import Tasks
from src.backend.utils import jsonify_task, oid, error_response


tasks_bp = Blueprint('tasks', __name__, url_prefix='/api')


@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    data = request.get_json()
    if not data:
        return error_response("Request body is required", 400)
    
    title = data.get('title', '').strip()
    if not title:
        return error_response("Title is required", 400)
    
    description = data.get('description', '').strip() or None
    status = data.get('status', 'todo')
    
    if status not in ['todo', 'in_progress', 'done']:
        return error_response("Invalid status", 400)
    
    task = Tasks.create(title, description, status)
    return jsonify(jsonify_task(task)), 201


@tasks_bp.route('/tasks', methods=['GET'])
def list_tasks():
    """List all tasks."""
    tasks = Tasks.find_all()
    return jsonify([jsonify_task(task) for task in tasks]), 200


@tasks_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task."""
    task_oid = oid(task_id)
    if not task_oid:
        return error_response("Invalid task ID", 400)
    
    task = Tasks.find_by_id(task_oid)
    if not task:
        return error_response("Task not found", 404)
    
    return jsonify(jsonify_task(task)), 200


@tasks_bp.route('/tasks/<task_id>', methods=['PATCH'])
def update_task(task_id):
    """Update a task."""
    task_oid = oid(task_id)
    if not task_oid:
        return error_response("Invalid task ID", 400)
    
    data = request.get_json()
    if not data:
        return error_response("Request body is required", 400)
    
    updates = {}
    
    if 'title' in data:
        title = data['title'].strip()
        if not title:
            return error_response("Title cannot be empty", 400)
        updates['title'] = title
    
    if 'description' in data:
        updates['description'] = data['description'].strip() or None
    
    if 'status' in data:
        if data['status'] not in ['todo', 'in_progress', 'done']:
            return error_response("Invalid status", 400)
        updates['status'] = data['status']
    
    if not updates:
        return error_response("At least one field is required", 400)
    
    task = Tasks.update(task_oid, updates)
    if not task:
        return error_response("Task not found", 404)
    
    return jsonify(jsonify_task(task)), 200


@tasks_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task and its comments."""
    task_oid = oid(task_id)
    if not task_oid:
        return error_response("Invalid task ID", 400)
    
    deleted = Tasks.delete(task_oid)
    if not deleted:
        return error_response("Task not found", 404)
    
    return '', 204