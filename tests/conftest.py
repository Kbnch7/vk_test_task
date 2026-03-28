import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_db():
    session = AsyncMock()
    mock_transaction = AsyncMock()
    mock_transaction.__aenter__ = AsyncMock(return_value=None)
    mock_transaction.__aexit__ = AsyncMock(return_value=None)
    session.begin = MagicMock(return_value=mock_transaction)
    
    return session