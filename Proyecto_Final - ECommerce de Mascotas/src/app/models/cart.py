import enum
import uuid

from sqlalchemy import CheckConstraint, Column, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.extensions import Base


class CartStatusEnum(enum.Enum):
    pending = "pending"
    completed = "completed"


class Cart(Base):
    __tablename__ = "carts"

    cart_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    status = Column(Enum(CartStatusEnum), nullable=False, default=CartStatusEnum.pending)

    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")


class CartItem(Base):
    __tablename__ = "cart_items"

    cart_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("carts.cart_id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    cart = relationship("Cart", back_populates="items")

    __table_args__ = (CheckConstraint("quantity > 0", name="check_cart_item_quantity_positive"),)
