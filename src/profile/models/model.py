from typing import List
from sqlalchemy import Column, ForeignKey, String, Text, Integer, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Profile(Base):
    __tablename__ = "profiles"
    profile_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    name: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    second_name: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    surname: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    about_me: Mapped[str | None] = mapped_column(String(400), nullable=True, default=None)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    number_phone: Mapped[str | None] = mapped_column(String(11), nullable=True, default=None)

    # Relationship: one-to-one with BuisnessForm
    business_form: Mapped["BuisnessForm"] = relationship(
        "BuisnessForm", back_populates="profile", uselist=False, lazy="select"
    )

    photos: Mapped[List["Photo"]] = relationship(
        back_populates="profile",
        lazy="select",
    )
    user: Mapped["User"] = relationship(
        back_populates="profile",
        lazy="joined",
    )


class BuisnessForm(Base):
    __tablename__ = "business_form"
    business_id: Mapped[int] = mapped_column(ForeignKey("profiles.profile_id", ondelete="CASCADE"), primary_key=True)
    buisness_form: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    form_of_ownership: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    size_shape: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    industry_form: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    geographical_coverage: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    type_of_clients: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    nature_of_the_organization: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    life_cycle: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    form_description: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)

    # Relationship: one-to-one with Profile
    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="business_form", lazy="select"
    )



class Photo(Base):
    __tablename__ = "photos"
    photo_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.profile_id", ondelete="CASCADE"))
    photo_type: Mapped[str] = mapped_column(String(5), nullable=False)
    photo_path: Mapped[str] = mapped_column(Text(), nullable=False)
    profile: Mapped["Profile"] = relationship(back_populates="photos")
