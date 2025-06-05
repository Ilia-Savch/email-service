import pytest
from core.schemas.user import UserRead, UserCreate, UserUpdate


def test_user_read_valid_data():
    data = {
        "id": 1,
        "email": "user@example.com",
        "is_active": True,
        "is_superuser": False,
        "is_verified": True,
    }
    user = UserRead.model_validate(data)
    assert user.email == "user@example.com"
    assert user.is_active is True


def test_user_create_missing_email_fails():
    data = {
        "password": "strongpassword123"
    }
    with pytest.raises(Exception):
        UserCreate.model_validate(data)


def test_user_update_partial_data():
    data = {
        "email": "newemail@example.com"
    }
    user_update = UserUpdate.model_validate(data)
    assert user_update.email == "newemail@example.com"
