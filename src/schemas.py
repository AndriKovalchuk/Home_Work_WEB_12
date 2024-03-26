from datetime import date, datetime
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, EmailStr, field_validator
import re
from typing import Optional


class ContactModel(BaseModel):
    first_name: str = Field(max_length=15)
    last_name: str = Field(max_length=15)
    email: EmailStr
    contact_number: str
    birth_date: date
    additional_information: str = Optional[str]

    @field_validator('contact_number')  # noqa
    @classmethod
    def validate_contact_number(cls, value: str) -> str:
        if not re.match(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$', value):
            """
            Matching formats:
            123-456-7890
            (123) 456-7890
            123 456 7890
            123.456.7890
            +12 (345) 678-9012
            """
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid contact number")
        return value

    @field_validator("birth_date")  # noqa
    @classmethod
    def validate_birth_date(cls, value: date) -> date:
        if value > date.today():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Invalid birth date. Birth date can't be in the future.")
        return value


class ContactResponse(ContactModel):
    id: int

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
