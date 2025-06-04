from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from core.models.access_token import AccessToken
from core.models.db_helper import db_helper

from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_tokens_db(
        session: Annotated["AsyncSession", Depends(db_helper.session_getter)]
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
