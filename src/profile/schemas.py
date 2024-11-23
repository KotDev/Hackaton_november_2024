import re
from datetime import datetime

from pydantic import BaseModel, field_validator
from pydantic.v1.utils import validate_field_name
from typing import Optional

from pydantic import BaseModel, field_validator
from typing import List, Optional
import re


class ProfileSchema(BaseModel):
    name: Optional[str] = None
    second_name: Optional[str] = None
    surname: Optional[str] = None
    about_me: Optional[str] = None
    age: Optional[int] = None
    number_phone: Optional[str] = None

    @field_validator("number_phone")
    def validate_number_phone(cls, value):
        if value and not re.match(r"^7\d{10}$", value):
            raise ValueError("Invalid phone number format")
        return value

    @field_validator("age")
    def validate_age(cls, value):
        if value is not None and not (18 <= value <= 100):
            raise ValueError("Age must be between 18 and 100")
        return value

    class Config:
        orm_mode = True


class BusinessFormSchema(BaseModel):
    profile_id: int
    buisness_form: Optional[str] = None
    form_of_ownership: Optional[str] = None
    size_shape: Optional[str] = None
    industry_form: Optional[str] = None
    geographical_coverage: Optional[str] = None
    type_of_clients: Optional[str] = None
    nature_of_the_organization: Optional[str] = None
    life_cycle: Optional[str] = None
    form_description: Optional[str] = None

    class Config:
        orm_mode = True

class UpdateBusinessFormSchema(BaseModel):
    buisness_form: Optional[str] = None
    form_of_ownership: Optional[str] = None
    size_shape: Optional[str] = None
    industry_form: Optional[str] = None
    geographical_coverage: Optional[str] = None
    type_of_clients: Optional[str] = None
    nature_of_the_organization: Optional[str] = None
    life_cycle: Optional[str] = None
    form_description: Optional[str] = None

    class Config:
        orm_mode = True


class ResponseProfileSchema(BaseModel):
    profile_id: int
    email: str
    profile: ProfileSchema


class GetProfile(BaseModel):
    profile_id: int

class PhotoSchema(BaseModel):
    profile_id: int
    photo_type: str
    photo_path: str

