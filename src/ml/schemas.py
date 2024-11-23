import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, model_validator, ValidationError, field_validator


class NewsSchema(BaseModel):
    news_id: int
    title: str
    link: str
    date: datetime

    model_config = {"from_attributes": True}

class TagsSchema(BaseModel):
    tag_id: int
    name: str

    model_config = {"from_attributes": True}

class ResponseNewsSchema(BaseModel):
    news: NewsSchema
    tags: List[TagsSchema]

class RibbonNewsSchema(BaseModel):
    ribbon: List[ResponseNewsSchema]

class FilterTagSchema(BaseModel):
    tags_filter: List[TagsSchema]


class BusinessSupportSchema(BaseModel):
    id: int
    name: str
    date_start: datetime
    date_end: datetime
    link: str

    model_config = {"from_attributes": True}

class BusinessSupportTagSchema(BaseModel):
    business_supports: List[BusinessSupportSchema]
    tags: List[TagsSchema]

class ResponseNewsSchema(BaseModel):
    news: NewsSchema
    tags: Optional[List[TagsSchema]]


class RibbonNewsSchema(BaseModel):
    ribbon: List[ResponseNewsSchema]

class RegisterSchema(BaseModel):
    email: str
    password: str
    password_verification: str
    role: str

    @field_validator("email")
    def validate_email(cls, email: str) -> str:
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Email is invalid")
        return email

    @field_validator("password")
    def validate_password_complexity(cls, password: str) -> str:
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", password):
            raise ValueError(
                "Password is not complex enough. Minimum eight characters, "
                "at least one letter, one number, and one special character"
            )
        return password

    @model_validator(mode="after")
    def validate_passwords_match(self) -> 'RegisterSchema':
        if not self.password and not self.password_verification and self.password != self.password_verification:
            raise ValueError("Passwords must match")
        return self

class SupportSchema(BaseModel):
    support_id: int
    title: str
    description: str
    link: Optional[str]
    date: datetime


class ResponseSupportSchema(BaseModel):
    support: SupportSchema
    tags: Optional[List[TagsSchema]]


class RibbonSupportSchema(BaseModel):
    ribbon: List[ResponseSupportSchema]



