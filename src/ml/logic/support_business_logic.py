from fastapi import HTTPException, Request, Depends
from ml.manager.managers import BusinessSupportManager, TagsManager
from profile.controllers.profile_conrollers import manager
from profile.schemas import GetProfile
from datetime import datetime
import locale
from ml.manager.managers import BusinessSupportManager

# Устанавливаем русскую локаль
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")


class BusinessSupportLogic:

    @staticmethod
    async def format_data_parser(data_pars: list[dict]):
        """
        Форматирует данные, проверяет существование записи и добавляет новую поддержку, если она отсутствует.
        """
        manager = BusinessSupportManager()
        for data in data_pars:
            # Попытка получить существующую поддержку по имени
            buisness_support = await manager.get_business_support(None, name=data["name"])
            buisness_support = buisness_support.scalars().first()

            # Если поддержка уже существует, пропускаем
            if buisness_support:
                continue

            # Преобразование даты из строки в datetime (если необходимо)
            if isinstance(data.get("date_start"), str):
                data["date_start"] = BusinessSupportLogic.parse_date(data["date_start"])
            if isinstance(data.get("date_end"), str):
                data["date_end"] = BusinessSupportLogic.parse_date(data["date_end"])

            # Добавляем новую запись
            await manager.add_business_support(data)

    @staticmethod
    def parse_date(date_str: str) -> datetime:
        """
        Преобразует строку даты в объект datetime.
        """
        try:
            return datetime.strptime(date_str, "%d %B %Y %H:%M")
        except ValueError:
            # Если час представлен однозначно, добавляем ведущий ноль
            try:
                date_str_fixed = date_str.replace(" ", " 0", 1) if " " in date_str.split()[2] else date_str
                return datetime.strptime(date_str_fixed, "%d %B %Y %H:%M")
            except ValueError as e:
                raise ValueError(f"Ошибка преобразования даты: {str(e)}")


    @staticmethod
    async def generate_ml_tag_for_business_support():
        manager_business_support = BusinessSupportManager()
        manager_tags = TagsManager()
        add_tags = []
        business_supports = await manager_business_support.get_business_supports_with_not_tags()
        if not business_supports:
            return
        for bs in business_supports:
            ## функция мл которая возвращаеи тег
            tags = []
            for tag in tags:
                if tag == "UnvariantText":
                    await manager_business_support.delete_business_support(support_id=bs.id)
                tag = await manager_tags.add_tag(tag)
                add_tags.append(tag.name)
            await manager_business_support.add_tags_to_support(support_id=bs.id, tags=add_tags)



    @staticmethod
    def get_user(request: Request) -> GetProfile:
        """
        Получает информацию о пользователе из запроса.
        """
        if not hasattr(request.state, "user"):
            raise HTTPException(status_code=401, detail="User not authenticated")
        usr = request.state.user
        schema = GetProfile(profile_id=usr.get("user_id"))
        return schema
