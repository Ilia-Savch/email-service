from core.types.user_id import UserIdType
from .base import Base
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTable
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[UserIdType]):
    user_id: Mapped[UserIdType] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="cascade"),
        nullable=False,
    )

    @classmethod
    def get_db(cls, session):
        return SQLAlchemyBaseAccessTokenTable(session, AccessToken)
