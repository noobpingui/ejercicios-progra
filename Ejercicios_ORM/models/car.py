
from models.base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum as sqlAlchemyEnum, ForeignKey
from enum import Enum as PyEnum
from typing import Optional


class CarStatus(str, PyEnum):
    available = 'available'
    unavailable = 'unavailable'

class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(100))
    model: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column()
    status: Mapped[CarStatus] = mapped_column(sqlAlchemyEnum(CarStatus))
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("lyfter_ORM_exercise.users.id"))

    #Para ver "bonito" el resultado de el objeto car cuando hago las pruebas en app.py
    def __repr__(self):
        return f"Car(id={self.id}, brand='{self.brand}', model='{self.model}',year='{self.year}',status='{self.status}',user_id='{self.user_id}')"