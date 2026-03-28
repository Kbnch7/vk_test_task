import uuid

from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

@patch("app.api.v1.users.create_user_service")
def test_create_user_endpoint(mock_service):
    fake_uuid = str(uuid.uuid4())
    mock_user = MagicMock()
    mock_user.id = fake_uuid
    mock_user.username = "test_user"
    mock_user.login = "test_user"
    mock_user.password = "decrypted_pass"
    
    mock_service.return_value = mock_user
    
    payload = {
        "login": "test_user",
        "password": "secure_password_123",
        "project_id": str(uuid.uuid4()),
        "env_id": str(uuid.uuid4()),
        "domain_id": str(uuid.uuid4())
    }
    
    response = client.post("/users/", json=payload)
    
    assert response.status_code == 201
    assert response.json()["id"] == fake_uuid

@patch("app.api.v1.users.get_users_service")
def test_get_users_endpoint(mock_service):
    mock_service.return_value = []
    
    response = client.get("/users/?limit=10")
    
    assert response.status_code == 200
    assert response.json() == []
