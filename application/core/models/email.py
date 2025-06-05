from core.models.base import Base
from sqlalchemy import String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Email(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    sent_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False)

    sender = relationship("User", back_populates="sent_emails")
    recipients: Mapped[
        list["EmailRecipient"]
    ] = relationship(back_populates="email")


class EmailRecipient(Base):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    email_id: Mapped[int] = mapped_column(
        ForeignKey("emails.id"), primary_key=True)
    recipient_email: Mapped[str] = mapped_column(String(320), nullable=False)

    email: Mapped["Email"] = relationship(back_populates="recipients")
