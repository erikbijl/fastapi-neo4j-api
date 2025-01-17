from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_node():
    response = client.post("/nodes/create_node/", json={
        "node_id": "123",
        "properties": {"name": "Test Node"}
    })
    assert response.status_code == 200
    assert "node_created" in response.json()

def test_count_nodes():
    response = client.get("/nodes/count_nodes/")
    assert response.status_code == 200
    assert "node_count" in response.json()

def test_delete_node():
    response = client.delete("/nodes/delete_node/", json={
        "node_id": "123"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Node deleted successfully"}
