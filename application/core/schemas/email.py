from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


class EmailRecipientBase(BaseModel):
    recipient_email: EmailStr


class EmailRecipientCreate(EmailRecipientBase):
    pass


class EmailBase(BaseModel):
    subject: str
    body: Optional[str] = Field(default=None)


class EmailCreate(EmailBase):
    recipients: List[EmailRecipientCreate]


class EmailRead(BaseModel):
    id: int
    subject: str
    body: str
    sender: str
    recipient: str
    created_at: datetime
    model_config = {"from_attributes": True}


class EmailFilterParams(BaseModel):
    date_from:  Optional[datetime] = Field(default=None)
    date_to:  Optional[datetime] = Field(default=None)
    sender: Optional[str] = Field(default=None)
    recipient: Optional[str] = Field(default=None)
    subject_contains: Optional[str] = Field(default=None)
