from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date


class ContactSchema(BaseModel):
    name: str
    surname: str
    phone_number: str
    email: EmailStr
    birthday: date
    notes: str


class ContactResponse(ContactSchema):
    id: int = 1

    class Config:
        from_attributes = True