
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum as sqlAlchemyEnum
from enum import Enum as PyEnum


class UserRoles(str, PyEnum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(250))
    password: Mapped[str] = mapped_column(String(250))
    user_role: Mapped[UserRoles] = mapped_column(sqlAlchemyEnum(UserRoles), default="user")


