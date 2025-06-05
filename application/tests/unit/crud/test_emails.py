import pytest

from api.api_v1.emails.crud import count_received_emails, count_sent_emails, get_filtered_emails, save_email_to_db
from core.models.email import Email
from unittest.mock import AsyncMock, MagicMock


@pytest.mark.asyncio
async def test_save_email_to_db(async_session_mock, fake_user, fake_email_create):
    email = await save_email_to_db(fake_email_create, async_session_mock, fake_user)

    async_session_mock.add.assert_any_call(email)
    async_session_mock.flush.assert_awaited_once()
    async_session_mock.commit.assert_awaited_once()

    assert email.subject == fake_email_create.subject
    assert email.body == fake_email_create.body
    assert email.sender_id == fake_user.id
    assert email.sent_at is not None


@pytest.mark.asyncio
async def test_get_filtered_emails(async_session_mock, fake_user, fake_email_filter_params, fake_email):

    mock_result = MagicMock()
    mock_result.unique.return_value.scalars.return_value.all.return_value = [
        fake_email]

    async_session_mock.execute = AsyncMock(return_value=mock_result)

    emails = await get_filtered_emails(async_session_mock, fake_user, fake_email_filter_params)

    async_session_mock.execute.assert_awaited_once()
    assert isinstance(emails, list)
    assert emails[0].id == fake_email.id


@pytest.mark.asyncio
async def test_count_sent_emails(async_session_mock, fake_user):
    mock_result = MagicMock()
    mock_result.scalar_one.return_value = 3

    async_session_mock.execute = AsyncMock(return_value=mock_result)

    count = await count_sent_emails(async_session_mock, fake_user)

    async_session_mock.execute.assert_awaited_once()
    assert count == 3


@pytest.mark.asyncio
async def test_count_received_emails(async_session_mock, fake_user):
    mock_result = MagicMock()
    mock_result.scalar_one.return_value = 7

    async_session_mock.execute = AsyncMock(return_value=mock_result)

    count = await count_received_emails(async_session_mock, fake_user)

    async_session_mock.execute.assert_awaited_once()
    assert count == 7
