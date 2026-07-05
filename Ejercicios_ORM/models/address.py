
from models.base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from typing import Optional

class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    province: Mapped[str] = mapped_column(String(150))
    city: Mapped[str] = mapped_column(String(150))
    street: Mapped[str] = mapped_column(String(150))
    additional_directions: Mapped[Optional[str]] = mapped_column(String(250))
    user_id : Mapped[int] = mapped_column(ForeignKey("lyfter_ORM_exercise.users.id"))

    #Para ver "bonito" el resultado de el objeto address cuando hago las pruebas en app.py
    def __repr__(self):
        return f"Address(id={self.id}, province='{self.province}', city='{self.city}',street='{self.street}',additional_directions='{self.additional_directions}', user_id='{self.user_id}')"
