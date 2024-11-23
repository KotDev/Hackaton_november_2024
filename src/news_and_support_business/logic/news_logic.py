from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup
from fastapi import HTTPException, Request
from fastapi.params import Depends

from news_and_support_business.manager.managers import NewsManager, TagsManager
from profile.schemas import GetProfile
from datetime import datetime
import locale
from news_and_support_business.models.models import News
from settings import parser


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
        paragraphs = []
        if content_section:
            paragraphs = [p.get_text(strip=True) for p in content_section.find_all('p')]

        return paragraphs

    @staticmethod
    async def generate_ml_tag_for_news():
        manager_news = NewsManager()
        manager_tags = TagsManager()
        add_tags = []
        news = await manager_news.get_news_with_not_tags()
        if not news:
            return
        for new in news:
            content = await NewsLogic.pars_news_info(new)
            ## функция мл которая возвращаеи тег
            tags = []
            for tag in tags:
                if tag == "UnvariantText":
                    await manager_news.delete_news(news_id=new.id)
                tag = await manager_tags.add_tag(tag)
                add_tags.append(tag.name)
            await manager_news.add_tags_to_news(news_id=new.id, tags=add_tags)


    @staticmethod
    def get_user(request: Request) -> GetProfile:
        if not hasattr(request.state, "user"):
            raise HTTPException(status_code=401, detail="User not authenticated")
        usr = request.state.user
        schema = GetProfile(profile_id=usr.get("user_id"))
        return schema