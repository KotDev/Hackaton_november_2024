from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base



buisness_support_tags = Table(
    "buisness_support_tags",
    Base.metadata,
    Column("buisness_support_id", ForeignKey("buisness_support.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


news_tags = Table(
    "news_tags",
    Base.metadata,
    Column("news_id", ForeignKey("news.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class BuisnessSupport(Base):
    __tablename__ = "buisness_support"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    date_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    link: Mapped[str | None] = mapped_column(String(500), nullable=True)

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=buisness_support_tags,
        back_populates="buisness_supports",
        lazy="select",
    )


class News(Base):
    __tablename__ = "news"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    link: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)


    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=news_tags,
        back_populates="news",
        lazy="select",
    )


class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)


    buisness_supports: Mapped[list["BuisnessSupport"]] = relationship(
        "BuisnessSupport",
        secondary=buisness_support_tags,
        back_populates="tags",
        lazy="select",
    )


    news: Mapped[list["News"]] = relationship(
        "News",
        secondary=news_tags,
        back_populates="tags",
        lazy="select",
    )


