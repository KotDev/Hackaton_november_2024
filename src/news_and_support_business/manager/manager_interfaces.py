from abc import ABC, abstractmethod

class BusinessSupportManagerInterface(ABC):

    @abstractmethod
    async def get_business_support(self, support_id: int | None, **kwargs):
        pass

    @abstractmethod
    async def update_business_support(self, support_id: int | None, update_data: dict, **kwargs):
        pass

    @abstractmethod
    async def delete_business_support(self, support_id: int | None, **kwargs):
        pass

    @abstractmethod
    async def add_business_support(self, schema):
        pass


class NewsManagerInterface(ABC):

    @abstractmethod
    async def get_news(self, news_id: int | None, **kwargs):
        pass

    @abstractmethod
    async def add_news(self, schema):
        pass

    @abstractmethod
    async def update_news(self, news_id: int | None, update_date: dict, **kwargs):
        pass

    @abstractmethod
    async def delete_news(self,  news_id: int | None, **kwargs):
        pass


class TagsManagerInterface(ABC):
    @abstractmethod
    async def get_tag(self, tag_id: int | None, **kwargs):
        pass

    @abstractmethod
    async def add_tag(self, name: str):
        pass

    @abstractmethod
    async def update_tag(self, tag_id: int | None, update_date: dict, **kwargs):
        pass

    @abstractmethod
    async def delete_tag(self, tag_id: int | None, **kwargs):
        pass