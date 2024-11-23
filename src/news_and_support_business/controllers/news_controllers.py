from fastapi import APIRouter, Depends, HTTPException, Query

from news_and_support_business.schemas import RibbonNewsSchema, FilterTagSchema, TagsSchema, ResponseNewsSchema, NewsSchema, CreateTagSchema
from news_and_support_business.manager.managers import NewsManager, TagsManager

router_news = APIRouter(prefix="/news", tags=["News"])


@router_news.get("/all_news")
async def get_all_news(tag_names: list[str] | None = Query(None), order_by: bool | None = Query(None),  news_manager: NewsManager = Depends(NewsManager)):
    """
    Получить всю ленту новостей вместе с тегами.
    """
    if not tag_names:
        news_with_tags = await news_manager.get_all_news_with_tags(order_by_date=order_by)
    else:
        news_with_tags = await news_manager.get_news_by_tags(tag_names, order_by)


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


