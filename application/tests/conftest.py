from fastapi import FastAPI
import pytest
import pytest_asyncio
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, MagicMock

from core.models.user import User
from core.models.email import Email, EmailRecipient
from core.schemas.email import EmailCreate, EmailFilterParams
from api.api_v1.auth.routers import router as auth_router


@pytest_asyncio.fixture
async def async_session_mock():
    session = AsyncMock()
    session.flush = AsyncMock()
    session.commit = AsyncMock()
    session.execute = AsyncMock()
    session.add = MagicMock()
    return session


@pytest_asyncio.fixture
async def fake_user() -> User:
    user = User()
    user.id = 1
    user.email = "user@example.com"
    user.is_active = True
    user.is_superuser = False
    user.is_verified = True
    return user


@pytest_asyncio.fixture
async def fake_email() -> Email:
    email = Email()
    email.id = 1
    email.sender_id = 1
    email.subject = "Test Subject"
    email.body = "Test Body"
    email.sent_at = datetime.now(timezone.utc)
    return email


@pytest_asyncio.fixture
async def fake_email_recipient() -> EmailRecipient:
    recipient = EmailRecipient()
    recipient.id = 1
    recipient.email_id = 1
    recipient.recipient_email = "recipient@example.com"
    return recipient


@pytest_asyncio.fixture
async def fake_email_create() -> EmailCreate:
    from core.schemas.email import EmailRecipientCreate

    return EmailCreate(
        subject="Test Subject",
        body="Test Body",
        recipients=[
            EmailRecipientCreate(recipient_email="recipient1@example.com"),
            EmailRecipientCreate(recipient_email="recipient2@example.com"),
        ],
    )


@pytest_asyncio.fixture
async def fake_email_filter_params() -> EmailFilterParams:
    return EmailFilterParams(
        date_from=None,
        date_to=None,
        subject_contains=None,
        sender=None,
        recipient=None,
    )


@pytest.fixture
def test_app():
    app = FastAPI()
    app.include_router(auth_router)
    return app
