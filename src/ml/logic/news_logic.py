from datetime import datetime

from fastapi import HTTPException, Request
from fastapi.params import Depends

from ml.manager.managers import NewsManager
from profile.schemas import GetProfile
from datetime import datetime
import locale

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
    def get_user(request: Request) -> GetProfile:
        if not hasattr(request.state, "user"):
            raise HTTPException(status_code=401, detail="User not authenticated")
        usr = request.state.user
        schema = GetProfile(profile_id=usr.get("user_id"))
        return schema