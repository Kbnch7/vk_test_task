import uuid
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.database.models import User
from app.schemas.users import UserCreate
from app.services.exceptions import (
    DatabaseError,
    NoAvailiableUserError,
    UserAlreadyExistsError,
)
from app.services.users import user_service


def get_valid_user_data(login="test_user@mail.ru"):
    return UserCreate(
        login=login,
        password="password",
        project_id=uuid.uuid4(),
        env_id=uuid.uuid4(),
        domain_id=uuid.uuid4()
    )

@pytest.mark.asyncio
async def test_create_user_success(mocker, mock_db):
    user_in = get_valid_user_data()
    fake_id = uuid.uuid4()

    mocker.patch("app.services.users.encrypt_password", return_value="hashed_password")
    mocker.patch(
        "app.services.users.decrypt_password",
        return_value="secure_password_123"
    )

    mock_user = User(id=fake_id, login="test_user", password="hashed_password")
    mocker.patch.object(
        user_service.repo,
        'create',
        new_callable=AsyncMock,
        return_value=mock_user
    )

    result = await user_service.create(mock_db, user_in)

    assert result.login == "test_user"
    assert result.id == fake_id
    user_service.repo.create.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_already_exists(mocker, mock_db):
    mocker.patch("app.services.users.encrypt_password")
    mocker.patch.object(
        user_service.repo,
        "create",
        side_effect=IntegrityError(None, None, None)
    )

    user_in = get_valid_user_data("existing_user@mail.ru")

    with pytest.raises(UserAlreadyExistsError):
        await user_service.create(mock_db, user_in)

@pytest.mark.asyncio
async def test_get_users_service(mocker, mock_db):
    mock_users = [User(id=uuid.uuid4()), User(id=uuid.uuid4())]

    mocker.patch.object(
        user_service.repo,
        'get_users',
        new_callable=AsyncMock,
        return_value=mock_users
    )
    mocker.patch("app.services.users.decrypt_users_password", return_value=mock_users)

    result = await user_service.get_users(mock_db, limit=10, skip=0)

    assert len(result) == 2
    user_service.repo.get_users.assert_called_once_with(mock_db, 10, 0)

@pytest.mark.asyncio
async def test_lock_user_success(mocker, mock_db):
    user_uuid = uuid.uuid4()
    mock_user = User(id=user_uuid, password="hashed")

    mocker.patch.object(
        user_service.repo,
        'lock_user',
        new_callable=AsyncMock,
        return_value=mock_user
    )
    mocker.patch("app.services.users.decrypt_password", return_value="decrypted")

    result = await user_service.lock_first_avaliable_user(mock_db, days_to_lock=1)

    assert result.id == user_uuid
    mock_db.begin.assert_called_once()

@pytest.mark.asyncio
async def test_lock_user_no_available(mocker, mock_db):
    mocker.patch.object(
        user_service.repo,
        'lock_user',
        new_callable=AsyncMock,
        return_value=None
    )

    with pytest.raises(NoAvailiableUserError):
        await user_service.lock_first_avaliable_user(mock_db)

@pytest.mark.asyncio
async def test_unlock_users_service(mocker, mock_db):
    mocker.patch.object(
        user_service.repo,
        'unlock_users',
        new_callable=AsyncMock,
        return_value=5
    )

    result = await user_service.unlock_users(mock_db)
    assert result == 5

@pytest.mark.asyncio
async def test_database_error_handling(mocker, mock_db):
    mocker.patch.object(
        user_service.repo,
        'unlock_users',
        side_effect=SQLAlchemyError()
    )

    with pytest.raises(DatabaseError):
        await user_service.unlock_users(mock_db)
