import re
from time import sleep
from typing import Any, Self

from pydantic import BaseModel, model_validator, ValidationError, field_validator
from datetime import datetime

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

class LoginSchema(BaseModel):
    email: str
    password: str

class AccessTokenSchema(BaseModel):
    user_id: int
    role: str
    token_type: str = "Access-Token"

class RefreshTokenSchema(BaseModel):
    user_id: int
    token_type: str = "Refresh-Token"

class UserSchema(BaseModel):
    user_id: int
    role: str

class JWTSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"