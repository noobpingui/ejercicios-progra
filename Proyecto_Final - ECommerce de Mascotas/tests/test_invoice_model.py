import uuid
from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.invoice import Invoice, InvoiceItem, InvoiceStatusEnum
from app.models.product import Product
from app.models.user import User


def _make_user(db_session):
    user = User(email=f"invoice-{uuid.uuid4().hex}@example.com", password_hash="hashed")
    db_session.add(user)
    db_session.commit()
    return user


def _make_product(db_session, price=Decimal("20.00")):
    product = Product(name="Cama para perro", price=price, stock=10)
    db_session.add(product)
    db_session.commit()
    return product


def _make_invoice(user):
    return Invoice(
        user_id=user.user_id,
        billing_street="Calle 123",
        billing_city="San Jose",
        billing_postal_code="10101",
        billing_country="Costa Rica",
        payment_method="SINPE",
    )


def test_create_invoice_defaults_to_completed(db_session):
    user = _make_user(db_session)

    invoice = _make_invoice(user)
    db_session.add(invoice)
    db_session.commit()

    assert isinstance(invoice.invoice_number, uuid.UUID)
    assert invoice.status == InvoiceStatusEnum.completed
    assert invoice.created_at is not None

    db_session.delete(invoice)
    db_session.delete(user)
    db_session.commit()


def test_invoice_item_price_at_purchase_is_frozen(db_session):
    user = _make_user(db_session)
    product = _make_product(db_session, price=Decimal("20.00"))
    invoice = _make_invoice(user)
    invoice.items.append(
        InvoiceItem(product_id=product.product_id, quantity=2, price_at_purchase=Decimal("20.00"))
    )
    db_session.add(invoice)
    db_session.commit()

    product.price = Decimal("35.00")
    db_session.commit()

    stored_item = db_session.query(InvoiceItem).filter_by(invoice_number=invoice.invoice_number).one()
    assert stored_item.price_at_purchase == Decimal("20.00")

    db_session.delete(stored_item)
    db_session.commit()
    db_session.delete(invoice)
    db_session.commit()
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_invoice_item_requires_positive_quantity(db_session):
    user = _make_user(db_session)
    product = _make_product(db_session)
    invoice = _make_invoice(user)
    db_session.add(invoice)
    db_session.commit()

    db_session.add(
        InvoiceItem(
            invoice_number=invoice.invoice_number,
            product_id=product.product_id,
            quantity=0,
            price_at_purchase=Decimal("20.00"),
        )
    )
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    db_session.delete(invoice)
    db_session.commit()
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()
