from typing import List
from sqlalchemy import Column, ForeignKey, String, Text, Integer, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

profile_buisness_form = Table(
    "profile_business_form",
    Base.metadata,
    Column("profile_id", ForeignKey("profiles.profile_id", ondelete="CASCADE"), primary_key=True),
    Column("business_form_id", ForeignKey("business_form.id", ondelete="CASCADE"), primary_key=True),
)

class Profile(Base):
    __tablename__ = "profiles"
    profile_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    name: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    second_name: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    surname: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    about_me: Mapped[str | None] = mapped_column(String(400), nullable=True, default=None)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    number_phone: Mapped[str | None] = mapped_column(String(11), nullable=True, default=None)

    # Relationships
    buisness_forms: Mapped[List["BuisnessForm"]] = relationship(
        secondary=profile_buisness_form,
        back_populates="profiles",
        lazy="select",
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
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    buisness_form: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    form_of_ownership: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    size_shape: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    industry_form: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    geographical_coverage: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    type_of_clients: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    nature_of_the_organization: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    life_cycle: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    form_description: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)

    # Relationships
    profiles: Mapped[List["Profile"]] = relationship(
        secondary=profile_buisness_form,
        back_populates="buisness_forms",
        lazy="select",
    )


class Photo(Base):
    __tablename__ = "photos"
    photo_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.profile_id", ondelete="CASCADE"))
    photo_type: Mapped[str] = mapped_column(String(5), nullable=False)
    photo_path: Mapped[str] = mapped_column(Text(), nullable=False)
    profile: Mapped["Profile"] = relationship(back_populates="photos")
