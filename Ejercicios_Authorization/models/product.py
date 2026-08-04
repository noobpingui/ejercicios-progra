

from models.base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric, func, Integer, DateTime

from decimal import Decimal
from datetime import datetime


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250))
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))

    # Stores both date and time, automatically populated on creation
    entry_date: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now())
    
    quantity: Mapped[int] = mapped_column(Integer)
    

    