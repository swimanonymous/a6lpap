"""Tests for comments API endpoints."""
import json
from src.backend.models import Tasks


def create_task(client, title="Test Task", description="Test Description", status="todo"):
    """Helper to create a task."""
    response = client.post('/api/tasks', 
                          data=json.dumps({
                              'title': title,
                              'description': description,
                              'status': status
                          }),
                          content_type='application/json')
    return response.get_json()


def test_create_comment_success(client):
    """Test creating a comment successfully."""
    task = create_task(client)
    task_id = task['_id']
    
    response = client.post(f'/api/tasks/{task_id}/comments',
                          data=json.dumps({
                              'body': 'Great work!',
                              'author': 'Ayush'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = response.get_json()
    
    # Assert shape
    assert '_id' in data
    assert data['task_id'] == task_id
    assert data['body'] == 'Great work!'
    assert data['author'] == 'Ayush'
    assert 'created_at' in data
    assert 'updated_at' in data


def test_create_comment_empty_body(client):
    """Test creating a comment with empty body fails."""
    task = create_task(client)
    task_id = task['_id']
    
    response = client.post(f'/api/tasks/{task_id}/comments',
                          data=json.dumps({
                              'body': '   ',
                              'author': 'Ayush'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_create_comment_no_body(client):
    """Test creating a comment without body fails."""
    task = create_task(client)
    task_id = task['_id']
    
    response = client.post(f'/api/tasks/{task_id}/comments',
                          data=json.dumps({
                              'author': 'Ayush'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_create_comment_task_not_found(client):
    """Test creating a comment for non-existent task."""
    response = client.post('/api/tasks/507f1f77bcf86cd799439011/comments',
                          data=json.dumps({
                              'body': 'Great work!'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data


def test_create_comment_invalid_task_id(client):
    """Test creating a comment with invalid task ID."""
    response = client.post('/api/tasks/invalid-id/comments',
                          data=json.dumps({
                              'body': 'Great work!'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_create_comment_without_author(client):
    """Test creating a comment without author is allowed."""
    task = create_task(client)
    task_id = task['_id']
    
    response = client.post(f'/api/tasks/{task_id}/comments',
                          data=json.dumps({
                              'body': 'Anonymous comment'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['body'] == 'Anonymous comment'
    assert data['author'] is None


def test_list_comments_success(client):
    """Test listing comments for a task."""
    task = create_task(client)
    task_id = task['_id']
    
    # Create multiple comments
    for i in range(5):
        client.post(f'/api/tasks/{task_id}/comments',
                   data=json.dumps({
                       'body': f'Comment {i}',
                       'author': f'User {i}'
                   }),
                   content_type='application/json')
    
    response = client.get(f'/api/tasks/{task_id}/comments')
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert 'comments' in data
    assert 'count' in data
    assert 'limit' in data
    assert 'offset' in data
    assert data['count'] == 5
    assert len(data['comments']) == 5
    assert data['limit'] == 20
    assert data['offset'] == 0


def test_list_comments_newest_first(client):
    """Test comments are returned newest first."""
    task = create_task(client)
    task_id = task['_id']
    
    # Create comments in order
    comments_created = []
    for i in range(3):
        response = client.post(f'/api/tasks/{task_id}/comments',
                              data=json.dumps({
                                  'body': f'Comment {i}'
                              }),
                              content_type='application/json')
        comments_created.append(response.get_json()['_id'])
    
    response = client.get(f'/api/tasks/{task_id}/comments')
    data = response.get_json()
    
    # Should be in reverse order (newest first)
    assert data['comments'][0]['_id'] == comments_created[2]
    assert data['comments'][1]['_id'] == comments_created[1]
    assert data['comments'][2]['_id'] == comments_created[0]


def test_list_comments_pagination(client):
    """Test comment pagination."""
    task = create_task(client)
    task_id = task['_id']
    
    # Create 25 comments
    for i in range(25):
        client.post(f'/api/tasks/{task_id}/comments',
                   data=json.dumps({'body': f'Comment {i}'}),
                   content_type='application/json')
    
    # Get first page
    response = client.get(f'/api/tasks/{task_id}/comments?limit=10&offset=0')
    data = response.get_json()
    
    assert data['count'] == 25
    assert len(data['comments']) == 10
    assert data['limit'] == 10
    assert data['offset'] == 0
    
    # Get second page
    response = client.get(f'/api/tasks/{task_id}/comments?limit=10&offset=10')
    data = response.get_json()
    
    assert data['count'] == 25
    assert len(data['comments']) == 10
    assert data['offset'] == 10


def test_list_comments_limit_max_100(client):
    """Test limit is clamped to 100."""
    task = create_task(client)
    task_id = task['_id']
    
    response = client.get(f'/api/tasks/{task_id}/comments?limit=200')
    data = response.get_json()
    
    assert data['limit'] == 100


def test_list_comments_invalid_pagination(client):
    """Test invalid pagination parameters."""
    task = create_task(client)
    task_id = task['_id']
    
    # Invalid limit
    response = client.get(f'/api/tasks/{task_id}/comments?limit=abc')
    assert response.status_code == 400
    
    # Invalid offset
    response = client.get(f'/api/tasks/{task_id}/comments?offset=xyz')
    assert response.status_code == 400
    
    # Negative offset
    response = client.get(f'/api/tasks/{task_id}/comments?offset=-5')
    assert response.status_code == 400


def test_list_comments_task_not_found(client):
    """Test listing comments for non-existent task."""
    response = client.get('/api/tasks/507f1f77bcf86cd799439011/comments')
    assert response.status_code == 404


def test_update_comment_body_success(client):
    """Test updating comment body."""
    task = create_task(client)
    task_id = task['_id']
    
    # Create comment
    response = client.post(f'/api/tasks/{task_id}/comments',
                          data=json.dumps({'body': 'Original'}),
                          content_type='application/json')
    comment_id = response.get_json()['_id']
    
    # Update comment
    response = client.patch(f'/api/comments/{comment_id}',
                           data=json.dumps({'body': 'Updated'}),
                           content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['body'] == 'Updated'


def test_update_comment_author_success(client):
    """Test updating comment author."""
    task = create_task(client)
    task_id = task['_id']
    
    # Create comment
    response = client.post(f'/api/tasks/{task_id}/comments',
                          data=json.dumps({'body': 'Test', 'author': 'Alice'}),
                          content_type='application/json')
    comment_id = response.get_json()['_id']
    
    # Update author
    response = client.patch(f'/api/comments/{comment_id}',
                           data=json.dumps({'author': 'Bob'}),
                           content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['author'] == 'Bob'
    assert data['body'] == 'Test'  # Body unchanged


def test_update_comment_both_fields(client):
    """Test updating both body and author."""
    task = create_task(client)
    task_id = task['_id']
    
    # Create comment
    response = client.post(f'/api/tasks/{task_id}/comments',
                          data=json.dumps({'body': 'Original', 'author': 'Alice'}),
                          content_type='application/json')
    comment_id = response.get_json()['_id']
    
    # Update both
    response = client.patch(f'/api/comments/{comment_id}',
                           data=json.dumps({'body': 'Updated', 'author': 'Bob'}),
                           content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['body'] == 'Updated'
    assert data['author'] == 'Bob'


def test_update_comment_empty_body(client):
    """Test updating with empty body fails."""
    task = create_task(client)
    task_id = task['_id']
    
    # Create comment
    response = client.post(f'/api/tasks/{task_id}/comments',
                          data=json.dumps({'body': 'Original'}),
                          content_type='application/json')
    comment_id = response.get_json()['_id']
    
    # Try to update with empty body
    response = client.patch(f'/api/comments/{comment_id}',
                           data=json.dumps({'body': '   '}),
                           content_type='application/json')
    
    assert response.status_code == 400


def test_update_comment_no_fields(client):
    """Test updating without any fields fails."""
    task = create_task(client)
    task_id = task['_id']
    
    # Create comment
    response = client.post(f'/api/tasks/{task_id}/comments',
                          data=json.dumps({'body': 'Original'}),
                          content_type='application/json')
    comment_id = response.get_json()['_id']
    
    # Try to update without fields
    response = client.patch(f'/api/comments/{comment_id}',
                           data=json.dumps({}),
                           content_type='application/json')
    
    assert response.status_code == 400


def test_update_comment_not_found(client):
    """Test updating non-existent comment."""
    response = client.patch('/api/comments/507f1f77bcf86cd799439011',
                           data=json.dumps({'body': 'Updated'}),
                           content_type='application/json')
    
    assert response.status_code == 404


def test_delete_comment_success(client):
    """Test deleting a comment."""
    task = create_task(client)
    task_id = task['_id']
    
    # Create comment
    response = client.post(f'/api/tasks/{task_id}/comments',
                          data=json.dumps({'body': 'To be deleted'}),
                          content_type='application/json')
    comment_id = response.get_json()['_id']
    
    # Delete comment
    response = client.delete(f'/api/comments/{comment_id}')
    assert response.status_code == 204
    
    # Verify deletion
    response = client.get(f'/api/tasks/{task_id}/comments')
    data = response.get_json()
    assert data['count'] == 0

def test_delete_comment_twice(client):
    """Test deleting the same comment twice returns 404."""
    task = create_task(client)
    task_id = task['_id']
    
    # Create comment
    response = client.post(f'/api/tasks/{task_id}/comments',
                          data=json.dumps({'body': 'To be deleted'}),
                          content_type='application/json')
    comment_id = response.get_json()['_id']
    
    # Delete first time
    response = client.delete(f'/api/comments/{comment_id}')
    assert response.status_code == 204
    
    # Delete second time should fail
    response = client.delete(f'/api/comments/{comment_id}')
    assert response.status_code == 404


def test_delete_comment_not_found(client):
    """Test deleting non-existent comment."""
    response = client.delete('/api/comments/507f1f77bcf86cd799439011')
    assert response.status_code == 404


def test_delete_comment_invalid_id(client):
    """Test deleting with invalid comment ID."""
    response = client.delete('/api/comments/invalid-id')
    assert response.status_code == 400


def test_cascade_delete_task_deletes_comments(client):
    """Test that deleting a task also deletes its comments."""
    task = create_task(client)
    task_id = task['_id']
    
    # Create multiple comments
    for i in range(3):
        client.post(f'/api/tasks/{task_id}/comments',
                   data=json.dumps({'body': f'Comment {i}'}),
                   content_type='application/json')
    
    # Verify comments exist
    response = client.get(f'/api/tasks/{task_id}/comments')
    assert response.get_json()['count'] == 3
    
    # Delete task
    response = client.delete(f'/api/tasks/{task_id}')
    assert response.status_code == 204
    
    # Verify task is deleted
    response = client.get(f'/api/tasks/{task_id}')
    assert response.status_code == 404