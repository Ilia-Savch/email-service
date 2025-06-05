import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from fastapi_users.authentication.strategy.db import DatabaseStrategy

from api.dependencies.auth.access_tokens import get_access_tokens_db
from api.dependencies.auth.strategy import get_database_strategy
from api.dependencies.auth.user_manager import get_user_manager

from api.dependencies.auth.users import get_users_db
from core.auth.user_manager import UserManager

from core.config import settings
from core.models.access_token import AccessToken
from core.models.user import User


@pytest.mark.asyncio
async def test_get_access_tokens_db():
    mock_session = AsyncMock()
    gen = get_access_tokens_db(mock_session)
    access_tokens_db = await anext(gen)

    from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
    assert isinstance(access_tokens_db, SQLAlchemyAccessTokenDatabase)


@pytest.mark.asyncio
async def test_get_database_strategy():
    mock_access_token_db = MagicMock()
    strategy = get_database_strategy(mock_access_token_db)

    from fastapi_users.authentication.strategy.db import DatabaseStrategy
    assert isinstance(strategy, DatabaseStrategy)


@pytest.mark.asyncio
async def test_get_users_db():
    mock_session = AsyncMock()
    gen = get_users_db(mock_session)
    user_db = await anext(gen)

    from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
    assert isinstance(user_db, SQLAlchemyUserDatabase)


@pytest.mark.asyncio
async def test_get_user_manager():
    mock_user_db = MagicMock()
    gen = get_user_manager(mock_user_db)
    user_manager = await anext(gen)

    assert isinstance(user_manager, UserManager)
    assert user_manager.user_db is mock_user_db
