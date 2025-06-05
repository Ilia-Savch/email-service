from core.models.email import Email
from core.models.mixins.int_id_pk import IntIdPkMixin
from core.types.user_id import UserIdType
from .base import Base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.orm import Mapped, relationship

from typing import List


class User(IntIdPkMixin, Base, SQLAlchemyBaseUserTable[UserIdType]):

    sent_emails: Mapped[List["Email"]] = relationship(
        back_populates="sender",
        cascade="all, delete-orphan",
    )

    @classmethod
    def get_db(cls, session):
        return SQLAlchemyUserDatabase(session, cls)
