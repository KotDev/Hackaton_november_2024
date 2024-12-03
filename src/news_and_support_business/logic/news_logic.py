from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup
from fastapi import HTTPException, Request
from fastapi.params import Depends

from ml.ml_tags import model
from news_and_support_business.manager.managers import NewsManager, TagsManager
from profile.schemas import GetProfile
from datetime import datetime
import locale
from news_and_support_business.models.models import News
from settings import parser
from ml.ml_tags import model as model_tag


class NewsLogic:
    # Устанавливаем русскую локаль
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

    @staticmethod
    def __parse_date(date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, "%d %B %Y %H:%M")
        except ValueError:
            # Добавляем ведущий ноль к однозначным часам
            date_str_fixed = date_str.replace(" ", " 0", 1) if " " in date_str.split()[2] else date_str
            return datetime.strptime(date_str_fixed, "%d %B %Y %H:%M")

    @staticmethod
    async def format_parse_data(parse_data: list[dict]):
        manager = NewsManager()
        for data in parse_data:
            # Преобразуем строку даты в datetime
            date_str = data["date"]
            try:
                data["date"] = NewsLogic.__parse_date(date_str)  # Парсинг с русским форматом даты
            except ValueError as e:
                print(f"Ошибка преобразования даты: {e}")
                continue

            # Проверяем наличие новости
            news = await manager.get_news(None, title=data["title"])
            news = news.scalars().first()
            if news:
                continue

            # Добавляем новость
            await manager.add_news(data)

    @staticmethod
    async def pars_news_info(news: News):
        url = news.link
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch news page. Status: {response.status}")
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')
        content_section = soup.find('section', class_='e-material__content')
        full_content = ""
        if content_section:
            # Объединяем все параграфы в одну строку с пробелами между ними
            full_content = " ".join(p.get_text(strip=True) for p in content_section.find_all('p'))

        return full_content

    @staticmethod
    async def generate_ml_tag_for_news():
        manager_news = NewsManager()
        manager_tags = TagsManager()
        news = await manager_news.get_news_with_not_tags()
        if not news:
            return


        for new in news:
            content = await NewsLogic.pars_news_info(new)
            print(f"{new.title} | {content}")
            tags = model_tag.analyze(new.title, content)

            # Убедимся, что анализатор вернул строки
            if not all(isinstance(tag, str) for tag in tags):
                continue  # Пропускаем обработку, если теги некорректны

            # Флаг для удаления новости
            if "Нерелевантный" in tags:
                await manager_news.delete_news(news_id=new.id)
                continue

            # Получаем существующие теги
            existing_tags_ = []
            for tag in tags:
                existing_tags = await manager_tags.get_tag(tag_id=None, name=tag)
                existing_tags = existing_tags.scalar()
                existing_tags_.append(existing_tags)
            existing_tag_names = {tag.name for tag in existing_tags_ if tag is not None}

            # Добавляем только новые теги
            new_tags = [tag for tag in tags if tag not in existing_tag_names]
            if new_tags:
                for tg in new_tags:
                    await manager_tags.add_tag(tg)

            # Добавляем связи между новостью и тегами
            await manager_news.add_tags_to_news(news_id=new.id, tags=tags)

    @staticmethod
    def get_user(request: Request) -> GetProfile:
        if not hasattr(request.state, "user"):
            raise HTTPException(status_code=401, detail="User not authenticated")
        usr = request.state.user
        schema = GetProfile(profile_id=usr.get("user_id"))
        return schema