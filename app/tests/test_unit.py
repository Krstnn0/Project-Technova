import pytest
from app.main import app

@pytest.fixture
def client():
    """Fixture untuk mensimulasikan HTTP Client Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check_unit(client):
    """Unit Test: Memastikan endpoint /health merespons status 200 dan data benar"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'UP'
    assert data['service'] == 'inventory-service'

def test_get_inventory_unit(client):
    """Unit Test: Memastikan endpoint GET /api/v1/inventory mengembalikan list inventaris"""
    response = client.get('/api/v1/inventory')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert isinstance(data['data'], list)

def test_add_inventory_validation_fail(client):
    """Unit Test: Memastikan kiriman payload yang rusak/salah akan ditolak (Status 400)"""
    bad_payload = {"name": "Switch Cisco"}
    response = client.post('/api/v1/inventory', json=bad_payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False