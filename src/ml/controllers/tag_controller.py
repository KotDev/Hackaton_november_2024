from fastapi import APIRouter, Depends, HTTPException, Query
from setuptools.extern import names
from typing import List, Optional

from ml.schemas import *
from ml.manager.managers import BusinessSupportManager, TagsManager


from ml.schemas import (
    BusinessSupportSchema,
    FilterTagSchema,
    TagsSchema,
)


router_support = APIRouter(prefix="/business-supports", tags=["Business Supports"])


@router_support.get("/all_supports")
async def get_all_supports(tag_names: Optional[List[str]] = Query(None),
                           support_manager: BusinessSupportManager = Depends(BusinessSupportManager)):
    """
    Получить всю поддержку бизнеса вместе с тегами.
    """
    if not tag_names:
        supports_with_tags = await support_manager.get_all_supports_with_tags()
    else:
        supports_with_tags = await support_manager.get_business_supports_by_tag(tag_names)

    ribbon = RibbonSupportSchema(ribbon=[
        ResponseSupportSchema(
            support=BusinessSupportSchema(
                support_id=support.id,
                name=support.name,
                description=support.description
            ),
            tags=[
                TagsSchema(tag_id=tag.id, name=tag.name) for tag in support.tags
            ] if support.tags else []
        ) for support in supports_with_tags
    ] if supports_with_tags else [])

    return ribbon


@router_support.post("/create_support")
async def create_business_support(support_data: BusinessSupportSchema,
                                  support_manager: BusinessSupportManager = Depends(BusinessSupportManager)):
    """
    Создать новую поддержку бизнеса.
    """
    new_support = await support_manager.add_business_support(support_data.dict())
    return {
        "support_id": new_support.id,
        "name": new_support.name,
        "description": new_support.description
    }


@router_support.post("/{support_id}/add_tags")
async def add_tags_to_support(support_id: int,
                              tags: List[str],
                              support_manager: BusinessSupportManager = Depends(BusinessSupportManager)):
    """
    Добавить теги к поддержке бизнеса.
    """
    updated_support = await support_manager.add_tags_to_support(support_id, tags)
    if not updated_support:
        raise HTTPException(status_code=404, detail="Business support not found")
    return {
        "support_id": updated_support.id,
        "tags": [tag.name for tag in updated_support.tags]
    }


@router_support.delete("/{support_id}")
async def delete_business_support(support_id: int,
                                  support_manager: BusinessSupportManager = Depends(BusinessSupportManager)):
    """
    Удалить поддержку бизнеса по ID.
    """
    deleted = await support_manager.delete_business_support(support_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Business support not found")
    return {"message": "Business support deleted successfully"}


router_tags = APIRouter(prefix="/tags", tags=["Tags"])


@router_tags.get("/")
async def get_all_tags(tags_manager: TagsManager = Depends(TagsManager)):
    """
    Получить все теги.
    """
    tags = await tags_manager.get_all_tags()
    return FilterTagSchema(tags_filter=[
        TagsSchema(tag_id=tag.id, name=tag.name) for tag in tags
    ] if tags else [])


@router_tags.post("/create")
async def create_tag(tag_name: str, tags_manager: TagsManager = Depends(TagsManager)):
    """
    Создать новый тег.
    """
    new_tag = await tags_manager.add_tag(tag_name)
    return {"tag_id": new_tag.id, "name": new_tag.name}
