import enum
import uuid

from sqlalchemy import CheckConstraint, Column, Enum, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import Base


class ProductStatusEnum(enum.Enum):
    active = "active"
    inactive = "inactive"


class Product(Base):
    __tablename__ = "products"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    status = Column(Enum(ProductStatusEnum), nullable=False, default=ProductStatusEnum.active)

    __table_args__ = (
        CheckConstraint("price > 0", name="check_price_positive"),
        CheckConstraint("stock >= 0", name="check_stock_non_negative"),
    )
