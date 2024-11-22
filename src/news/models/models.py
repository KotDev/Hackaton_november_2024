from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime
from database import Base
from sqlalchemy import Table, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from typing import List

news_tags = Table(
    "news_tags",
    Base.metadata,
    Column("news_id", ForeignKey("news.news_id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.tag_id", ondelete="CASCADE"), primary_key=True),
)

class News(Base):
    news_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_news: Mapped[str] = mapped_column(String(200), nullable=False)
    url_news: Mapped[Text] = mapped_column(Text, nullable=False)
    start_date: Mapped[DateTime] = mapped_column(DateTime, nullable= False)
    end_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    news: Mapped[List["News"]] = relationship(
        "News", secondary=news_tags, back_populates="tags"
    )


class Tag(Base):
    tag_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary=news_tags, back_populates="news"
    )


