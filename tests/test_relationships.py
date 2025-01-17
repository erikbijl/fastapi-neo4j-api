from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_relationship():
    response = client.post("/relationships/add_relationship/", json={
        "node1_id": "123",
        "node2_id": "456",
        "relationship_type": "FRIEND"
    })
    assert response.status_code == 200
    assert "relationship_created" in response.json()

def test_count_relationship_per_type():
    response = client.delete("/relationships/count_relationship_per_type/", json={
        "relationship_type": "FRIEND"
    })
    assert response.status_code == 200
    assert "relationship_count" in response.json()

def test_remove_relationship():
    response = client.delete("/relationships/remove_relationship/", json={
        "node1_id": "123",
        "node2_id": "456",
        "relationship_type": "FRIEND"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Relationship removed successfully"}
