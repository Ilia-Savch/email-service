from fastapi import APIRouter
from .dependencies import fastapi_users

from core.config import settings
from core.schemas.user import UserCreate, UserRead

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],

)
# /me, /{id}
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserCreate
    )
)
