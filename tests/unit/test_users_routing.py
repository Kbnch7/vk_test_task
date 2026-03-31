import uuid
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.services.users import user_service

client = TestClient(app)

@patch.object(user_service, 'create', new_callable=AsyncMock)
def test_create_user_endpoint(mock_service):
    fake_uuid = str(uuid.uuid4())
    mock_user = MagicMock()
    mock_user.id = fake_uuid
    mock_user.login = "test_user@mail.ru"
    mock_user.password = "decrypted_pass"

    mock_service.return_value = mock_user

    payload = {
        "login": "test_user@mail.ru",
        "password": "secure_password_123",
        "project_id": str(uuid.uuid4()),
        "env_id": str(uuid.uuid4()),
        "domain_id": str(uuid.uuid4())
    }

    response = client.post("/api/v1/users/", json=payload)

    assert response.status_code == 201
    assert response.json()["id"] == fake_uuid

@patch.object(user_service, 'get_users', new_callable=AsyncMock)
def test_get_users_endpoint(mock_service):
    mock_service.return_value = []

    response = client.get("/api/v1/users/?limit=10")

    assert response.status_code == 200
    assert response.json() == []
