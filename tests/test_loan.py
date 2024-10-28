import pytest
from app.models.loan import Loan

def test_calculate_eligibility(client, auth_headers):
    response = client.post('/api/v1/loan/calculate-eligibility', headers=auth_headers)
    assert response.status_code == 200
    assert 'eligible' in response.json

def test_calculate_payment(client, auth_headers):
    response = client.post('/api/v1/loan/calculate-payment', 
        headers=auth_headers,
        json={
            'loan_amount': 1000000,
            'duration': 20
        })
    assert response.status_code == 200
    assert 'monthly_payment' in response.json