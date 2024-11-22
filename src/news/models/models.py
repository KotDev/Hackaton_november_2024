from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from database import Base

class News(Base):
    news_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_news: Mapped[str] = mapped_column(String(200), nullable=False)
    url_news: Mapped[Text] = mapped_column(Text, nullable=False)

