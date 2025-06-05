from fastapi import Depends
from fastapi_users.authentication.strategy.db import DatabaseStrategy
from core.config import settings

from .access_tokens import get_access_tokens_db


def get_database_strategy(
        access_token_db=Depends(get_access_tokens_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, settings.access_token.lifetime_seconds)
