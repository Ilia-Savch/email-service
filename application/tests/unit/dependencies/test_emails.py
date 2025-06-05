from datetime import datetime
from api.api_v1.emails.dependencies import get_email_filters
from core.schemas.email import EmailFilterParams


def test_get_email_filters_all_none():
    filters = get_email_filters()
    assert isinstance(filters, EmailFilterParams)
    assert filters.date_from is None
    assert filters.date_to is None
    assert filters.sender is None
    assert filters.recipient is None
    assert filters.subject_contains is None


def test_get_email_filters_with_values():
    date_from = datetime(2024, 1, 1)
    date_to = datetime(2024, 1, 31)
    sender = "sender@example.com"
    recipient = "recipient@example.com"
    subject_contains = "urgent"

    filters = get_email_filters(
        date_from=date_from,
        date_to=date_to,
        sender=sender,
        recipient=recipient,
        subject_contains=subject_contains
    )

    assert filters.date_from == date_from
    assert filters.date_to == date_to
    assert filters.sender == sender
    assert filters.recipient == recipient
    assert filters.subject_contains == subject_contains
