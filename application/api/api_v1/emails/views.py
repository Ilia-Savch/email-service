from datetime import datetime
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from api.api_v1.emails.crud import count_received_emails, count_sent_emails, get_filtered_emails, save_email_to_db
from .dependencies import get_email_filters
from core.models.db_helper import db_helper
from core.schemas.email import EmailCreate, EmailFilterParams, EmailRead
from core.utils.email_smtp import send_email_smtp
from core.models.user import User
from api.api_v1.users.dependencies import current_user
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["Email"], prefix=settings.api.v1.emails,)


@router.get(
    "",
    response_model=List[EmailRead],
    status_code=status.HTTP_200_OK,
)
async def get_emails(
    filters: Annotated[EmailFilterParams, Depends(get_email_filters)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(current_user)],
):
    emails = await get_filtered_emails(
        session=session, current_user=current_user, filters=filters)
    return [
        EmailRead(
            id=email.id,
            subject=email.subject,
            body=email.body,
            sender=email.sender.email,
            recipient=", ".join([r.recipient_email for r in email.recipients]),
            created_at=email.sent_at,
        )
        for email in emails
    ]


@router.post("/send", status_code=status.HTTP_201_CREATED)
async def send_email(
    email_data: EmailCreate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(current_user)],
):
    try:
        await send_email_smtp(
            to=[r.recipient_email for r in email_data.recipients],
            subject=email_data.subject,
            body=email_data.body,
            sender=current_user.email,
            smtp_host=settings.email_server.hostname,
            smtp_port=settings.email_server.port
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to send email")

    email = await save_email_to_db(email_data, session, current_user)
    return {"message": "Email sent", "email_id": email.id}


@router.get("/stats")
async def get_email_stats(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: Annotated[User, Depends(current_user)],
    date_from: Annotated[Optional[datetime], Query()] = None,
    date_to: Annotated[Optional[datetime], Query()] = None,
):
    sent_count = await count_sent_emails(session, current_user, date_from, date_to)
    received_count = await count_received_emails(session, current_user, date_from, date_to)

    return {
        "sent": sent_count,
        "received": received_count,
        "from": date_from,
        "to": date_to,
    }
