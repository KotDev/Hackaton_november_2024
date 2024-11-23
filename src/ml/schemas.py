import re
from datetime import datetime
from typing import List

from pydantic import BaseModel, field_validator


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






