import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_inventory_creation_integration(client):
    """
    Integration Test: 
    1. Ambil jumlah inventaris awal.
    2. Tambahkan item baru via POST.
    3. Ambil ulang inventaris via GET untuk memastikan item bertambah & data tersimpan secara terintegrasi.
    """

    initial_res = client.get('/api/v1/inventory')
    initial_data = initial_res.get_json()['data']
    initial_count = len(initial_data)

    new_item = {
        "name": "Access Point Aruba",
        "quantity": 15
    }
    post_res = client.post('/api/v1/inventory', json=new_item)
    assert post_res.status_code == 201
    assert post_res.get_json()['data']['name'] == "Access Point Aruba"

    final_res = client.get('/api/v1/inventory')
    final_data = final_res.get_json()['data']
    assert len(final_data) == initial_count + 1
    assert any(item['name'] == "Access Point Aruba" for item in final_data)