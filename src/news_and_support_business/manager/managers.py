from sqlalchemy import select, not_, exists, insert
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
            async with session.begin():
                # Получаем объект поддержки бизнеса
                result = await session.execute(
                    select(BuisnessSupport)
                    .options(joinedload(BuisnessSupport.tags))  # Явно подгружаем связанные теги
                    .where(BuisnessSupport.id == support_id)
                )
                support = result.scalars().first()

                if not support:
                    raise ValueError(f"BusinessSupport with ID {support_id} not found.")

                # Получаем имена существующих тегов за один запрос
                existing_tags = await session.execute(
                    select(Tag)
                    .where(Tag.name.in_(tags))  # Используем только имена тегов
                )
                existing_tags = existing_tags.scalars().all()

                # Множество имен существующих тегов
                existing_tag_names = {tag.name for tag in existing_tags}

                # Добавляем только новые теги
                new_tags = [tag for tag in tags if tag not in existing_tag_names]

                # Добавляем новые теги в базу данных
                for tag_name in new_tags:
                    tag = Tag(name=tag_name)  # Создаем новый объект Tag
                    session.add(tag)

                # Добавляем существующие теги к поддержке бизнеса
                for tag in existing_tags:
                    if tag not in support.tags:
                        support.tags.append(tag)  # Добавляем только те, которых еще нет

                # Добавляем новые теги к поддержке бизнеса
                for tag_name in new_tags:
                    # Нужно выполнить запрос, чтобы получить новый объект тега
                    new_tag = await session.execute(select(Tag).filter(Tag.name == tag_name))
                    new_tag = new_tag.scalars().first()
                    if new_tag and new_tag not in support.tags:
                        support.tags.append(new_tag)  # Добавляем связь с новым тегом

            # Сохраняем изменения
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
                .where(~News.tags.any())  # Проверяем отсутствие тегов
            )
            result = await session.execute(query)
            return result.scalars().all()

    from sqlalchemy.orm import joinedload

    async def add_tags_to_news(self, news_id: int, tags: list[str]):
        async with self.async_session() as session:
            async with session.begin():
                # Загружаем новость с тегами
                result = await session.execute(
                    select(News)
                    .options(joinedload(News.tags))  # Явно подгружаем связанные теги
                    .where(News.id == news_id)
                )
                news = result.scalars().first()
                if not news:
                    raise ValueError(f"News with ID {news_id} not found.")

                for tag_name in tags:
                    tag_result = await session.execute(select(Tag).where(Tag.name == tag_name))
                    tag = tag_result.scalars().first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        session.add(tag)

                    if tag not in news.tags:
                        news.tags.append(tag)

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

    async def add_tag(self, tag_name):
        async with self.async_session() as session:
            # Проверяем, существует ли уже тег
            existing_tag = await session.execute(
                select(Tag).where(Tag.name == tag_name)
            )
            existing_tag = existing_tag.scalar_one_or_none()

            if existing_tag:
                return existing_tag  # Возвращаем уже существующий тег

            # Если нет, добавляем новый
            new_tag = Tag(name=tag_name)
            session.add(new_tag)
            await session.commit()
            await session.refresh(new_tag)
            return new_tag

    async def get_all_tags(self):
        async with self.async_session() as session:
            query = select(Tag)
            result = await session.execute(query)
            return result.scalars().all()

