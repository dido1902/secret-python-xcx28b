import pytest
from app import create_app, db
from app.models.user import User
from app.models.property import Property
from app.models.loan import Loan
from app.models.cooperative import Cooperative, CooperativeMember
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    JWT_SECRET_KEY = 'test-secret-key'

@pytest.fixture
def app():
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    # Create test user
    user = User(email='test@example.com')
    user.set_password('testpass123')
    db.session.add(user)
    db.session.commit()
    
    # Login and get token
    response = client.post('/api/v1/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    token = response.json['access_token']
    
    return {'Authorization': f'Bearer {token}'}