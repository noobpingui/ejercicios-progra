from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum as sqlAlchemyEnum
from enum import Enum as PyEnum

class UserStatus(str, PyEnum):
    active = "active"
    inactive = "inactive"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150))
    status: Mapped[UserStatus] = mapped_column(sqlAlchemyEnum(UserStatus))

    #Para ver "bonito" el resultado de el objeto user cuando hago las pruebas en app.py
    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', status='{self.status}')"