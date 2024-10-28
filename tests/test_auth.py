import pytest
from app.models.user import User

def test_register(client):
    response = client.post('/api/v1/auth/register', json={
        'email': 'new@example.com',
        'password': 'testpass123'
    })
    assert response.status_code == 201
    assert User.query.filter_by(email='new@example.com').first() is not None

def test_login(client):
    # Create user
    user = User(email='test@example.com')
    user.set_password('testpass123')
    db.session.add(user)
    db.session.commit()
    
    # Test login
    response = client.post('/api/v1/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_get_profile(client, auth_headers):
    response = client.get('/api/v1/auth/profile', headers=auth_headers)
    assert response.status_code == 200
    assert 'email' in response.json