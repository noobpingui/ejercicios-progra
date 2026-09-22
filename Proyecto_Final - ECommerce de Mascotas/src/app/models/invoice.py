import enum
import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, Column, DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.extensions import Base


class InvoiceStatusEnum(enum.Enum):
    completed = "completed"
    partially_returned = "partially_returned"
    fully_returned = "fully_returned"


class Invoice(Base):
    __tablename__ = "invoices"

    invoice_number = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    status = Column(Enum(InvoiceStatusEnum), nullable=False, default=InvoiceStatusEnum.completed)

    billing_street = Column(String(255), nullable=False)
    billing_city = Column(String(255), nullable=False)
    billing_postal_code = Column(String(20), nullable=False)
    billing_country = Column(String(100), nullable=False)

    payment_method = Column(String(50), nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    items = relationship("InvoiceItem", back_populates="invoice")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    invoice_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_number = Column(UUID(as_uuid=True), ForeignKey("invoices.invoice_number"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Numeric(10, 2), nullable=False)

    invoice = relationship("Invoice", back_populates="items")

    __table_args__ = (CheckConstraint("quantity > 0", name="check_invoice_item_quantity_positive"),)
