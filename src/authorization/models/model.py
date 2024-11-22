from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from sqlalchemy.types import String, Text
from database import Base

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[Text] = mapped_column(Text(), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False)

    def __repr__(self):
        return f"User(user_id={self.user_id}, email='{self.email}', role='{self.role}, password: {self.password}')"