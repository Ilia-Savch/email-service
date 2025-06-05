from datetime import datetime
from typing import Optional, Annotated

from fastapi import Query

from core.schemas.email import EmailFilterParams


def get_email_filters(
    date_from: Annotated[Optional[datetime], Query()] = None,
    date_to: Annotated[Optional[datetime], Query()] = None,
    sender: Annotated[Optional[str], Query()] = None,
    recipient: Annotated[Optional[str], Query()] = None,
    subject_contains: Annotated[Optional[str], Query()] = None,
) -> EmailFilterParams:
    return EmailFilterParams(
        date_from=date_from,
        date_to=date_to,
        sender=sender,
        recipient=recipient,
        subject_contains=subject_contains,
    )
