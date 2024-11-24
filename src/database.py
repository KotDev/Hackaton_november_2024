from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from redis import Redis
from settings import database, redis, settings
from sqlalchemy.orm import declarative_base


class DataBase:
    def __init__(self):
        self.setting = database
        self.engine = create_async_engine(url=database.url_db, echo=database.echo)
        self.async_session = async_sessionmaker(
                                           bind=self.engine,
                                           class_=AsyncSession,
                                           expire_on_commit=database.expire_on_commit,
                                           autoflush=database.autoflush,
                                           autocommit=database.autocommit
                                                )

    def get_filters(self, obj, kwargs) -> list:
        """
        Метод формирования фильтра для объекта
        :param obj:
        :param kwargs:
        :return:
        """
        filter_params: list[str] = self.__get_filter_params(obj)
        if not any(param in kwargs for param in filter_params):
            raise ValueError("The required parameter filter was not found")
        filters = [getattr(obj, key) == value for key, value in kwargs.items() if key in filter_params]
        return filters

    @staticmethod
    def __get_filter_params(obj):
        """
        Метод возвращает параметры полей по котором можно отфильтровать объект
        :param obj:
        :return:
        """
        filter_params = list()
        params: dict = vars(obj).get('__annotations__')
        if params:
            for param in params.keys():
                filter_params.append(param)
            return filter_params
        raise ValueError("Object is not object model")

    @staticmethod
    def get_primary_key_field(model):
        """
        Возвращает атрибут, соответствующий первичному ключу в модели SQLAlchemy.

        :param model: Класс SQLAlchemy (например, User или Profile).
        :return: Поле первичного ключа (например, User.id).
        """
        primary_key_columns = model.__mapper__.primary_key
        if primary_key_columns:
            return primary_key_columns[0].key
        raise ValueError(f"Model {model.__name__} has no primary key defined.")


    async def delete_obj(self, id_obj: int | None, obj, **kwargs):
        async with self.async_session() as session:
            # Получаем имя первичного ключа
            primary_key_field = DataBase.get_primary_key_field(obj)

            if id_obj:
                # Если id_obj передано, удаляем объект с этим id
                result = await session.execute(
                    select(obj).filter(getattr(obj, primary_key_field) == id_obj, **kwargs)
                )
                objects = result.scalars().all()
                if not objects:
                    raise ValueError(f"{obj.__name__} with {primary_key_field} {id_obj} not found")
                # Прямое удаление
                await session.execute(
                    delete(obj).filter(getattr(obj, primary_key_field) == id_obj, **kwargs)
                )
            else:
                # Если id_obj не передано, удаляем по другим фильтрам
                result = await session.execute(
                    select(obj).filter_by(**kwargs)
                )
                objects = result.scalars().all()
                if not objects:
                    raise ValueError(f"{obj.__name__} not found with filters {kwargs}")
                # Прямое удаление
                await session.execute(
                    delete(obj).filter_by(**kwargs)
                )

            # Коммитим изменения в базе данных
            await session.commit()

    async def update_obj(self, id_obj: int | None, obj, update_data: dict, **kwargs):
        """
        Удаляет объект из бд id_obj - первичный ключ obj - Таблица, **kwargs - параметры фильтра для обновления
        update_data - словарь полей объекта и его новых значений
        :param id_obj:
        :param obj:
        :param update_data:
        :param kwargs:
        :return:
        """
        async with self.async_session() as session:
            objects = await self.get_obj(id_obj, obj, **kwargs)
            objects = objects.scalars().all()
            if not objects:
                raise ValueError(f"{obj.__name__} is not found")
            for object_model in objects:
                for key, val in update_data.items():
                    if hasattr(object_model, key):
                        setattr(object_model, key, val)
                    else:
                        raise ValueError(f"Attribute '{key}' does not exist on {obj.__name__} model")
            await session.commit()
            return objects

    async def get_obj(self, id_obj: int | None, obj, **kwargs):
        """
        Удаляет объект из бд id_obj - первичный ключ obj - Таблица,
        **kwargs - параметры фильтра для получения объекта из бд
        :param id_obj:
        :param obj:
        :param kwargs:
        :return:
        """
        async with self.async_session() as session:
            if id_obj is None:
                filters = self.get_filters(obj, kwargs)
                query = select(obj).where(*filters)
                result = await session.execute(query)
                return result
        pk_field = self.get_primary_key_field(obj)
        query = select(obj).where(getattr(obj, pk_field) == id_obj)
        result = await session.execute(query)
        return result

class BaseManager(DataBase):
    def __init__(self, base) -> None:
        super().__init__()
        self.base = base

    async def clear_models(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(self.base.metadata.drop_all)

    async def init_models(self) -> None:
        async with self.engine.begin() as conn:
             await conn.run_sync(self.base.metadata.create_all)


Base = declarative_base()
redis_client = Redis(host=redis.host, port=redis.port, db=redis.db, decode_responses=redis.decode_responses)