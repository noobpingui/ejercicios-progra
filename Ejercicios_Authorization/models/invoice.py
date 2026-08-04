
from models.base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Numeric, Integer, func, DateTime

from decimal import Decimal
from datetime import datetime





class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)

    quantity: Mapped[int] = mapped_column(Integer)
    total_price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))

    purchase_date: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now())

    user_id : Mapped[int] = mapped_column(ForeignKey("lyfter_authentication_exercise.users.id"))
    product_id : Mapped[int] = mapped_column(ForeignKey("lyfter_authentication_exercise.products.id"))

