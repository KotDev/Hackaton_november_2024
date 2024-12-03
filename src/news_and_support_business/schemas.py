import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, model_validator, ValidationError, field_validator


class NewsSchema(BaseModel):
    news_id: int
    title: str
    description: str
    link: str
    date: datetime

    model_config = {"from_attributes": True}


class CreateTagBusinessSupportSchema(BaseModel):
    tag_id: int
    business_support_id: int

class CreateTagNewsSchema(BaseModel):
    tag_id: int
    news_id: int

class CreateTagSchema(BaseModel):
    name: str

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
    description: str
    date_start: datetime
    date_end: datetime
    link: str

    model_config = {"from_attributes": True}

class BusinessSupportTagSchema(BaseModel):
    business_supports: List[BusinessSupportSchema]
    tags: List[TagsSchema]

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




