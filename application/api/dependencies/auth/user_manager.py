from fastapi import Depends
from .users import get_users_db
from core.auth.user_manager import UserManager


async def get_user_manager(user_db=Depends(get_users_db)):
    yield UserManager(user_db)
