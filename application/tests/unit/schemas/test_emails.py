import pytest
from datetime import datetime
from pydantic import ValidationError
from core.schemas.email import (
    EmailRecipientBase,
    EmailRecipientCreate,
    EmailBase,
    EmailCreate,
    EmailRead,
    EmailFilterParams,
)


def test_email_recipient_base_valid():
    data = {"recipient_email": "test@example.com"}
    recipient = EmailRecipientBase(**data)
    assert recipient.recipient_email == "test@example.com"


def test_email_recipient_base_invalid_email():
    data = {"recipient_email": "not-an-email"}
    with pytest.raises(ValidationError):
        EmailRecipientBase(**data)


def test_email_base_defaults():
    data = {"subject": "Hello"}
    email = EmailBase(**data)
    assert email.subject == "Hello"
    assert email.body is None


def test_email_create_requires_recipients():
    data = {
        "subject": "Subject",
        "body": "Body text",
        "recipients": [{"recipient_email": "user@example.com"}],
    }
    email_create = EmailCreate(**data)
    assert len(email_create.recipients) == 1
    assert email_create.recipients[0].recipient_email == "user@example.com"


def test_email_create_invalid_recipients():
    data = {
        "subject": "Subject",
        "body": "Body text",
        "recipients": [{"recipient_email": "invalid-email"}],
    }
    with pytest.raises(ValidationError):
        EmailCreate(**data)


def test_email_read_model_validate():
    class DummyEmail:
        def __init__(self):
            self.id = 1
            self.subject = "Test subject"
            self.body = "Test body"
            self.sender = "sender@example.com"
            self.recipient = "recipient@example.com"
            self.created_at = datetime(2024, 1, 1, 12, 0, 0)

    dummy = DummyEmail()
    email_read = EmailRead.model_validate(dummy)

    assert email_read.id == 1
    assert email_read.subject == "Test subject"
    assert email_read.body == "Test body"
    assert email_read.sender == "sender@example.com"
    assert email_read.recipient == "recipient@example.com"
    assert email_read.created_at == datetime(2024, 1, 1, 12, 0, 0)


def test_email_filter_params_defaults():
    params = EmailFilterParams()
    assert params.date_from is None
    assert params.date_to is None
    assert params.sender is None
    assert params.recipient is None
    assert params.subject_contains is None


def test_email_filter_params_valid_dates():
    data = {
        "date_from": "2024-01-01T00:00:00Z",
        "date_to": "2024-02-01T00:00:00Z",
    }
    params = EmailFilterParams(**data)
    assert params.date_from.isoformat() == "2024-01-01T00:00:00+00:00"
    assert params.date_to.isoformat() == "2024-02-01T00:00:00+00:00"
