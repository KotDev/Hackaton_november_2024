import re
from datetime import datetime

from pydantic import BaseModel, field_validator
from pydantic.v1.utils import validate_field_name


class ProfileSchema(BaseModel):
    name: str | None = None
    second_name: str | None = None
    surname: str | None = None
    about_me: str | None = None
    age: int | None = None
    number_phone: str | None = None

    @field_validator("number_phone")
    def validate_number_phone(cls, number_phone: str) -> str | None:
        if number_phone is None:
            return number_phone
        if not re.match(r'^7\d{10}$', number_phone):
            raise ValueError("Phone number is invalid")
        return number_phone

    @field_validator("age")
    def validate_age(cls, age: int) -> int | None:
        if age is None:
            return age
        if 18 <= age <= 100:
            return age
        raise ValueError("Age is invalid")

    model_config = {"from_attributes": True}

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

