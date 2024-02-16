from typing import Optional
from datetime import datetime, date

from pydantic import BaseModel, EmailStr, Field


class ContactSchema(BaseModel):
    name: str
    surname: str
    phone_number: str
    email: EmailStr
    birthday: date
    notes: Optional[str] = None


class ContactResponse(ContactSchema):
    id: int = 1

    class Config:
        from_attributes = True