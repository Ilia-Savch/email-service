from datetime import datetime, timezone
from fastapi import Query
from sqlalchemy import and_, func, select, or_
from sqlalchemy.orm import joinedload

from core.models.email import Email, EmailRecipient
from core.models.user import User
from core.schemas.email import EmailCreate, EmailFilterParams
from sqlalchemy.ext.asyncio import AsyncSession
from api.api_v1.users.dependencies import current_user

from typing import Annotated, List, Optional


async def save_email_to_db(
    email_data: EmailCreate, session: AsyncSession,  current_user: User,
) -> Email:
    email = Email(
        sender_id=current_user.id,
        subject=email_data.subject,
        body=email_data.body,
        sent_at=datetime.now(timezone.utc),
    )
    session.add(email)
    await session.flush()

    for r in email_data.recipients:
        session.add(EmailRecipient(
            email_id=email.id,
            recipient_email=r.recipient_email,
        ))

    await session.commit()
    return email


async def get_filtered_emails(
    session: AsyncSession,
    current_user: User,
    filters: EmailFilterParams,
) -> List[Email]:

    stmt = (
        select(Email)
        .options(joinedload(Email.recipients))
        .where(
            or_(
                Email.sender_id == current_user.id,
                Email.recipients.any(
                    EmailRecipient.recipient_email == current_user.email),
            )
        )
    )
    conditions = []

    if filters.date_from:
        conditions.append(Email.sent_at >= filters.date_from)
    if filters.date_to:
        conditions.append(Email.sent_at <= filters.date_to)
    if filters.subject_contains:
        conditions.append(Email.subject.ilike(f"%{filters.subject_contains}%"))
    if filters.sender:
        conditions.append(Email.sender.has(
            User.email.ilike(f"%{filters.sender}%")))
    if filters.recipient:
        conditions.append(Email.recipients.any(
            EmailRecipient.recipient_email.ilike(f"%{filters.recipient}%")))

    if conditions:
        stmt = stmt.where(and_(*conditions))

    result = await session.execute(stmt)
    emails = result.unique().scalars().all()
    return emails


async def count_sent_emails(
    session: AsyncSession,
    current_user: User,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
) -> int:
    conditions = [Email.sender_id == current_user.id]
    if date_from:
        conditions.append(Email.sent_at >= date_from)
    if date_to:
        conditions.append(Email.sent_at <= date_to)

    stmt = select(func.count(Email.id)).where(and_(*conditions))
    result = await session.execute(stmt)
    return result.scalar_one()


async def count_received_emails(
    session: AsyncSession,
    current_user: User,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
) -> int:
    conditions = [EmailRecipient.recipient_email == current_user.email]
    stmt = (
        select(func.count(EmailRecipient.id))
        .join(Email, Email.id == EmailRecipient.email_id)
        .where(and_(*conditions))
    )
    if date_from:
        stmt = stmt.where(Email.sent_at >= date_from)
    if date_to:
        stmt = stmt.where(Email.sent_at <= date_to)

    result = await session.execute(stmt)
    return result.scalar_one()
