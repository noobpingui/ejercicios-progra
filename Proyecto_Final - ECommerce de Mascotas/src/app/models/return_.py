import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.extensions import Base


class Return(Base):
    __tablename__ = "returns"

    return_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_number = Column(UUID(as_uuid=True), ForeignKey("invoices.invoice_number"), nullable=False)
    returned_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    items = relationship("ReturnItem", back_populates="return_")


class ReturnItem(Base):
    __tablename__ = "return_items"

    return_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    return_id = Column(UUID(as_uuid=True), ForeignKey("returns.return_id"), nullable=False)
    invoice_item_id = Column(
        UUID(as_uuid=True), ForeignKey("invoice_items.invoice_item_id"), nullable=False
    )
    quantity = Column(Integer, nullable=False)

    return_ = relationship("Return", back_populates="items")

    __table_args__ = (CheckConstraint("quantity > 0", name="check_return_item_quantity_positive"),)
