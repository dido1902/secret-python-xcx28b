import pytest
from app.models.cooperative import Cooperative, CooperativeMember

def test_create_cooperative(client, auth_headers):
    response = client.post('/api/v1/cooperative/cooperatives', 
        headers=auth_headers,
        json={
            'name': 'Test Cooperative',
            'description': 'Test Description'
        })
    assert response.status_code == 201
    assert Cooperative.query.first() is not None

def test_join_cooperative(client, auth_headers):
    # Create cooperative
    coop = Cooperative(name='Test Cooperative', admin_id=1)
    db.session.add(coop)
    db.session.commit()
    
    response = client.post(f'/api/v1/cooperative/cooperatives/{coop.id}/join',
        headers=auth_headers)
    assert response.status_code == 200
    assert CooperativeMember.query.first() is not None

def test_send_message(client, auth_headers):
    # Create and join cooperative
    coop = Cooperative(name='Test Cooperative', admin_id=1)
    db.session.add(coop)
    db.session.commit()
    
    member = CooperativeMember(cooperative_id=coop.id, user_id=1)
    db.session.add(member)
    db.session.commit()
    
    response = client.post(f'/api/v1/cooperative/cooperatives/{coop.id}/messages',
        headers=auth_headers,
        json={'content': 'Test message'})
    assert response.status_code == 201