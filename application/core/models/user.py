from core.models.mixins.int_id_pk import IntIdPkMixin
from core.types.user_id import UserIdType
from .base import Base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase


class User(IntIdPkMixin, Base, SQLAlchemyBaseUserTable[UserIdType]):

    @classmethod
    def get_db(cls, session):
        return SQLAlchemyUserDatabase(session, cls)
