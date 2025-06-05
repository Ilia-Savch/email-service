from api.dependencies.auth.backend import auth_backend
from fastapi import APIRouter

from core.config import settings
from core.schemas.user import UserCreate, UserRead

from ..users.dependencies import fastapi_users

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=['Auth']
)

# /login, /logout
router.include_router(
    router=fastapi_users.get_auth_router(auth_backend,),
    # required_verification=True,
)

# /register
router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate,),
)
