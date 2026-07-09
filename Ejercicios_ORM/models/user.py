from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum as sqlAlchemyEnum
from enum import Enum as PyEnum

#Para evitar importacion circular en tiempo de ejecucion. Necesario para usar relationship()
#Car
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.car import Car
#Address
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.address import Address

class UserStatus(str, PyEnum):
    active = "active"
    inactive = "inactive"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150))
    status: Mapped[UserStatus] = mapped_column(sqlAlchemyEnum(UserStatus))


    #To try relationship() with Car
    cars: Mapped[list["Car"]] = relationship(back_populates="user")
    #To try relationship() with Address
    addresses: Mapped[list["Address"]] = relationship(back_populates="user")

    #Para ver "bonito" el resultado de el objeto user cuando hago las pruebas en app.py
    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', status='{self.status}')"