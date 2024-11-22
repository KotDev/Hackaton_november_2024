from typing import List

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Profile(Base):
    __tablename__ = "profiles"
    profile_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    name: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    second_name: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    surname: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    about_me: Mapped[str | None] = mapped_column(String(400), nullable=True, default=None)
    age: Mapped[int | None] = mapped_column(nullable=True, default=None)
    number_phone: Mapped[str | None] = mapped_column(String(11), nullable=True, default=None)
    photos: Mapped[List["Photo"]] = relationship(back_populates="profile")
    user: Mapped["User"] = relationship(back_populates="profile")

class Photo(Base):
    __tablename__ = "photos"
    photo_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.profile_id", ondelete="CASCADE"))
    photo_type: Mapped[str] = mapped_column(String(5), nullable=False)
    photo_path: Mapped[str] = mapped_column(Text(), nullable=False)
    profile: Mapped["Profile"] = relationship(back_populates="photos")