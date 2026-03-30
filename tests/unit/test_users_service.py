import uuid

import pytest
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.services.users import (
    create_user_service, 
    get_users_service, 
    lock_first_avaliable_user_service, 
    unlock_users_service
)
from app.services.exceptions import UserAlreadyExistsError, DatabaseError, NoAvailiableUserError
from app.schemas.users import UserCreate
from app.database.models import User


def get_valid_user_data(login="test_user@mail.ru"):
    return UserCreate(
        login=login,
        password="password",
        project_id=uuid.uuid4(),
        env_id=uuid.uuid4(),
        domain_id=uuid.uuid4()
    )

@pytest.mark.asyncio
@patch("app.services.users.create_user_repo")
@patch("app.services.users.encrypt_password")
@patch("app.services.users.decrypt_password")
async def test_create_user_success(
    mock_decrypt, mock_encrypt, mock_repo, mock_db
):
    user_in = get_valid_user_data()
    mock_encrypt.return_value = "hashed_password"
    
    mock_user = User(id=uuid.uuid4(), login="test_user", password="hashed_password")
    mock_repo.return_value = mock_user
    mock_decrypt.return_value = "secure_password_123"

    result = await create_user_service(mock_db, user_in)

    assert result.login == "test_user"
    mock_repo.assert_called_once()

@pytest.mark.asyncio
@patch("app.services.users.create_user_repo")
@patch("app.services.users.encrypt_password")
async def test_create_user_already_exists(
    mock_encrypt, mock_repo, mock_db
):
    user_in = get_valid_user_data("existing_use@mail.ri")
    mock_repo.side_effect = IntegrityError(None, None, None)

    with pytest.raises(UserAlreadyExistsError):
        await create_user_service(mock_db, user_in)

@pytest.mark.asyncio
@patch("app.services.users.get_users_repo")
@patch("app.services.users.decrypt_users_password")
async def test_get_users_service(
    mock_decrypt_list, mock_repo, mock_db
):
    mock_repo.return_value = [User(id=1), User(id=2)]
    mock_decrypt_list.return_value = [User(id=1), User(id=2)]

    result = await get_users_service(mock_db, limit=10, skip=0)

    assert len(result) == 2
    mock_repo.assert_called_once_with(mock_db, 10, 0)

@pytest.mark.asyncio
@patch("app.services.users.lock_user_repo")
@patch("app.services.users.decrypt_password")
async def test_lock_user_success(
    mock_decrypt, mock_repo, mock_db
):
    user_uuid = uuid.uuid4()
    mock_user = User(id=user_uuid, password="hashed")
    mock_repo.return_value = mock_user
    mock_decrypt.return_value = "decrypted"

    result = await lock_first_avaliable_user_service(mock_db, days_to_lock=1)

    assert result.id == user_uuid
    mock_db.begin.assert_called_once()

@pytest.mark.asyncio
@patch("app.services.users.lock_user_repo")
async def test_lock_user_no_available(
    mock_repo, mock_db
):
    mock_repo.return_value = None

    with pytest.raises(NoAvailiableUserError):
        await lock_first_avaliable_user_service(mock_db)

@pytest.mark.asyncio
@patch("app.services.users.unlock_users_repo")
async def test_unlock_users_service(
    mock_repo, mock_db
):
    mock_repo.return_value = 5
    result = await unlock_users_service(mock_db)
    assert result == 5

@pytest.mark.asyncio
@patch("app.services.users.unlock_users_repo")
async def test_database_error_handling(
    mock_repo, mock_db
):
    mock_repo.side_effect = SQLAlchemyError()

    with pytest.raises(DatabaseError):
        await unlock_users_service(mock_db)
