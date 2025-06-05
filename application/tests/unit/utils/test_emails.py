import pytest
from unittest.mock import patch, AsyncMock
from core.utils.email_smtp import send_email_smtp


@pytest.mark.asyncio
@patch("core.utils.email_smtp.aiosmtplib.send", new_callable=AsyncMock)
async def test_send_email_smtp_success(mock_send):
    to = ["test1@example.com", "test2@example.com"]
    subject = "Test Subject"
    body = "Test Body"
    sender = "sender@example.com"
    smtp_host = "smtp.example.com"
    smtp_port = 587
    smtp_user = "user"
    smtp_password = "pass"

    await send_email_smtp(
        to=to,
        subject=subject,
        body=body,
        sender=sender,
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        smtp_user=smtp_user,
        smtp_password=smtp_password,
    )

    assert mock_send.call_count == 1

    sent_msg = mock_send.call_args.args[0]
    assert sent_msg["From"] == sender
    assert sent_msg["To"] == ", ".join(to)
    assert sent_msg["Subject"] == subject
    assert sent_msg.get_content().strip() == body

    kwargs = mock_send.call_args.kwargs
    assert kwargs["hostname"] == smtp_host
    assert kwargs["port"] == smtp_port
    assert kwargs["username"] == smtp_user
    assert kwargs["password"] == smtp_password
    assert kwargs["start_tls"] is False
