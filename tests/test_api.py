
import pytest
from api import create_app, db
from api.models import User
from api.tasks import generate_bio # Import the task to be mocked

@pytest.fixture(scope='function') # Changed from 'module' to 'function' for test isolation
def test_client():
    """Create a test client for the application."""
    app = create_app()
    app.config['TESTING'] = True
    # Use an in-memory SQLite database for fast, isolated tests
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all() # Create all tables
            yield testing_client  # This is where the testing happens
            db.drop_all() # Clean up the database

def test_get_all_users_empty(test_client):
    """Test GET /users when the database is empty."""
    response = test_client.get('/users')
    assert response.status_code == 200
    assert response.json == []

def test_create_user(test_client):
    """Test POST /users to create a new user."""
    data = {'username': 'newuser', 'email': 'new@example.com'}
    response = test_client.post('/users', json=data)
    assert response.status_code == 201
    assert response.json['username'] == 'newuser'
    assert 'id' in response.json

    # Verify the user was actually created in the db
    user = User.query.filter_by(username='newuser').first()
    assert user is not None

def test_create_user_invalid_data(test_client):
    """Test POST /users with invalid data (missing email)."""
    data = {'username': 'invaliduser'}
    response = test_client.post('/users', json=data)
    assert response.status_code == 400

def test_get_user_by_id(test_client):
    """Test GET /users/<id> for an existing user."""
    user = User(username='testget', email='testget@example.com')
    db.session.add(user)
    db.session.commit()

    response = test_client.get(f'/users/{user.id}')
    assert response.status_code == 200
    assert response.json['username'] == 'testget'

def test_get_user_not_found(test_client):
    """Test GET /users/<id> for a user that does not exist."""
    response = test_client.get('/users/999')
    assert response.status_code == 404

def test_update_user(test_client):
    """Test PUT /users/<id> to update a user."""
    user = User(username='testupdate', email='testupdate@example.com')
    db.session.add(user)
    db.session.commit()

    data = {'username': 'updateduser'}
    response = test_client.put(f'/users/{user.id}', json=data)
    assert response.status_code == 200
    assert response.json['username'] == 'updateduser'

    # Verify the update in the db
    updated = db.session.get(User, user.id)
    assert updated.username == 'updateduser'

def test_delete_user(test_client):
    """Test DELETE /users/<id> to remove a user."""
    user = User(username='testdelete', email='testdelete@example.com')
    db.session.add(user)
    db.session.commit()

    response = test_client.delete(f'/users/{user.id}')
    assert response.status_code == 204

    # Verify the user is gone from the db
    deleted_user = db.session.get(User, user.id)
    assert deleted_user is None

# --- New Test for Celery Task Endpoint ---
def test_generate_bio_endpoint(test_client, monkeypatch):
    """Test POST /users/<id>/generate-bio to trigger a celery task."""
    # 1. Setup: Create a user in the test database
    user = User(username='testbio', email='testbio@example.com')
    db.session.add(user)
    db.session.commit()

    # 2. Mock: Create a tracker and a mock function for the Celery task's .delay()
    mock_calls = []
    def mock_delay(*args, **kwargs):
        mock_calls.append({'args': args, 'kwargs': kwargs})
        class MockAsyncResult:
            id = "mock_task_id_12345"
        return MockAsyncResult()

    # Use monkeypatch to replace the real .delay with our mock
    monkeypatch.setattr(generate_bio, 'delay', mock_delay)

    # 3. Action: Call the API endpoint
    response = test_client.post(f'/users/{user.id}/generate-bio')

    # 4. Assert: Check the results
    assert response.status_code == 202 # Changed from 200 to 202 ACCEPTED
    assert response.json['message'] == 'Bio generation started.'
    assert 'task_id' in response.json

    # Verify our mocked task was called exactly once and with the correct user_id
    assert len(mock_calls) == 1
    assert mock_calls[0]['args'][0] == user.id # Changed from kwargs to args
