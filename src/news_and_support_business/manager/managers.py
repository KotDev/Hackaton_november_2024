from sqlalchemy import select, not_, exists
from sqlalchemy.orm import relationship, joinedload

from database import DataBase
from news_and_support_business.manager.manager_interfaces import TagsManagerInterface, NewsManagerInterface, BusinessSupportManagerInterface
from news_and_support_business.models.models import Tag, News, news_tags, BuisnessSupport, buisness_support_tags
from sqlalchemy import or_

class BusinessSupportManager(DataBase, BusinessSupportManagerInterface):
    def __init__(self):
        super().__init__()

    async def get_business_support(self, support_id: int | None, **kwargs):
        return await self.get_obj(support_id, BuisnessSupport, **kwargs)

    async def update_business_support(self, support_id: int | None, update_data: dict, **kwargs):
        return await self.update_obj(support_id, BuisnessSupport, update_data, **kwargs)

    async def delete_business_support(self, support_id: int | None, **kwargs):
        return await self.delete_obj(support_id, BuisnessSupport, **kwargs)

    async def add_business_support(self, schema: dict):
        async with self.async_session() as session:
            new_support = BuisnessSupport(**schema)
            session.add(new_support)
            await session.commit()
            return new_support

    async def get_business_supports_by_tag(self, tag_name: str):
        """
        Получить все поддержи бизнеса, связанные с указанным тегом.
        """
        async with self.async_session() as session:
            query = (
                select(BuisnessSupport)
                .join(buisness_support_tags)
                .join(Tag)
                .where(Tag.name == tag_name)
            )
            result = await session.execute(query)
            return result.scalars().all()

    async def get_business_supports_with_not_tags(self):
        async with self.async_session() as session:
            query = (
                select(BuisnessSupport)
                .outerjoin(buisness_support_tags, buisness_support_tags.c.buisness_support_id == BuisnessSupport.id)
                .where(buisness_support_tags.c.tag_id == None)
            )
            result = await session.execute(query)
            return result.scalars().all()

    async def get_all_supports_with_tags(self):
        """
        Получить все поддержки бизнеса и связанные с ними теги.
        """
        async with self.async_session() as session:
            query = select(BuisnessSupport).options(relationship("tags", lazy="joined"))
            result = await session.execute(query)
            return result.scalars().all()

    async def add_tags_to_support(self, support_id: int, tags: list[str]):
        """
        Добавить теги к поддержке бизнеса.
        """
        async with self.async_session() as session:
            support = await self.get_obj(support_id, BuisnessSupport)
            support = support.scalars().first()
            if not support:
                raise ValueError(f"BusinessSupport with ID {support_id} not found.")
            for tag_name in tags:
                tag = await session.get(Tag, {"name": tag_name})
                if not tag:
                    tag = Tag(name=tag_name)
                support.tags.append(tag)
            await session.commit()
            return support


class NewsManager(DataBase, NewsManagerInterface):
    def __init__(self):
        super().__init__()

    async def get_news(self, news_id: int | None, **kwargs):
        return await self.get_obj(news_id, News, **kwargs)

    async def update_news(self, news_id: int | None, update_data: dict, **kwargs):
        return await self.update_obj(news_id, News, update_data, **kwargs)

    async def delete_news(self, news_id: int | None, **kwargs):
        return await self.delete_obj(news_id, News, **kwargs)

    async def add_news(self, schema: dict):
        async with self.async_session() as session:
            new_news = News(**schema)
            session.add(new_news)
            await session.commit()
            return new_news

    async def get_news_by_tags(self, tag_names: list[str], order_by_date: bool | None = None):
        """
        Получить все новости, связанные с указанными тегами.
        :param tag_names: Список имен тегов.
        :param order_by_date: None - без сортировки, True - по убыванию даты, False - по возрастанию даты.
        """
        async with self.async_session() as session:
            query = (
                select(News)
                .join(news_tags)
                .join(Tag)
                .where(Tag.name.in_(tag_names))  # Ищем новости с любым из указанных тегов
                .distinct()  # Убираем дубликаты, если новость связана с несколькими тегами
            )

            if order_by_date is not None:
                if order_by_date:
                    query = query.order_by(News.date.desc())
                else:
                    query = query.order_by(News.date.asc())

            result = await session.execute(query)
            return result.scalars().all()

    async def get_all_news_with_tags(self, order_by_date: bool | None = None):
        """
        Получить все новости и связанные с ними теги.
        :param order_by_date: None - без сортировки, True - по убыванию даты, False - по возрастанию даты.
        """
        async with self.async_session() as session:
            query = select(News).options(joinedload(News.tags))

            if order_by_date is not None:
                if order_by_date:
                    query = query.order_by(News.date.desc())  # Сортировка по убыванию
                else:
                    query = query.order_by(News.date.asc())  # Сортировка по возрастанию

            result = await session.execute(query)
            return result.scalars().unique().all()


    async def get_news_with_not_tags(self):
        async with self.async_session() as session:
            query = (
                select(News)
                .options(joinedload(News.tags))  # Подгружаем связанные теги
                .where(~News.tags.any())  # Проверяем отсутствие тегов
            )
            result = await session.execute(query)
            return result.scalars().all()


    async def add_tags_to_news(self, news_id: int, tags: list[str]):
        """
        Добавить теги к новости.
        """
        async with self.async_session() as session:
            news = await self.get_obj(news_id, News)
            news = news.scalars().first()
            if not news:
                raise ValueError(f"News with ID {news_id} not found.")
            for tag_name in tags:
                tag = await session.get(Tag, {"name": tag_name})
                if not tag:
                    tag = Tag(name=tag_name)
                news.tags.append(tag)
            await session.commit()
            return news


class TagsManager(DataBase, TagsManagerInterface):
    def __init__(self):
        super().__init__()

    async def get_tag(self, tag_id: int | None, **kwargs):
        return await self.get_obj(tag_id, Tag, **kwargs)

    async def update_tag(self, tag_id: int | None, update_data: dict, **kwargs):
        return await self.update_obj(tag_id, Tag, update_data, **kwargs)

    async def delete_tag(self, tag_id: int | None, **kwargs):
        return await self.delete_obj(tag_id, Tag, **kwargs)

    async def add_tag(self, name: str):
        """
        Добавить новый тег.
        """
        async with self.async_session() as session:
            tag = Tag(name=name)
            session.add(tag)
            await session.commit()
            return tag

    async def get_all_tags(self):
        async with self.async_session() as session:
            query = select(Tag)
            result = await session.execute(query)
            return result.scalars().all()

