from fastapi import APIRouter, Depends, HTTPException, Query
from setuptools.extern import names

from ml.schemas import RibbonNewsSchema, FilterTagSchema, TagsSchema, ResponseNewsSchema, NewsSchema
from ml.manager.managers import NewsManager, TagsManager

router_news = APIRouter(prefix="/news", tags=["News"])


@router_news.get("/all_news")
async def get_all_news(tag_names: list[str] | None = Query(None),  news_manager: NewsManager = Depends(NewsManager)):
    """
    Получить всю ленту новостей вместе с тегами.
    """
    if not tag_names:
        news_with_tags = await news_manager.get_all_news_with_tags()
    else:
        news_with_tags = await news_manager.get_news_by_tags(tag_names)


    ribbon = RibbonNewsSchema(ribbon=[ResponseNewsSchema(news=NewsSchema(news_id=news.id,
                                                                         title=news.title,
                                                                         link=news.link,
                                                                         date=news.date),
                                tags=[TagsSchema(tag_id=tag.id, name=tag.name) for tag in news.tags]
                                if news.tags else []) for news in news_with_tags] if news_with_tags else [])

    return ribbon



@router_news.get("/tags")
async def get_tags(tags_manager: TagsManager = Depends(TagsManager)):
    tags = await tags_manager.get_all_tags()
    return FilterTagSchema(tags_filter=[TagsSchema(tag_id=tag.id, name=tag.name) for tag in tags] if tags else [])


@router_news.post("/create_tag")
async def create_tag_for_news(tag_name: str, tags_manager: TagsManager = Depends(TagsManager)):
    """
    Создать тег для новостей.
    """
    tag = await tags_manager.add_tag(tag_name)
    return {"tag_id": tag.id, "name": tag.name}
