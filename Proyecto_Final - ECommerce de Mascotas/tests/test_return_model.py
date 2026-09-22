import uuid
from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.invoice import Invoice, InvoiceItem
from app.models.product import Product
from app.models.return_ import Return, ReturnItem
from app.models.user import User


def _make_user(db_session):
    user = User(email=f"return-{uuid.uuid4().hex}@example.com", password_hash="hashed")
    db_session.add(user)
    db_session.commit()
    return user


def _make_product(db_session):
    product = Product(name="Juguete", price=Decimal("15.00"), stock=10)
    db_session.add(product)
    db_session.commit()
    return product


def _make_invoice_item(db_session, user, product, quantity=3):
    invoice = Invoice(
        user_id=user.user_id,
        billing_street="Calle 1",
        billing_city="San Jose",
        billing_postal_code="10101",
        billing_country="Costa Rica",
        payment_method="SINPE",
    )
    invoice_item = InvoiceItem(product_id=product.product_id, quantity=quantity, price_at_purchase=product.price)
    invoice.items.append(invoice_item)
    db_session.add(invoice)
    db_session.commit()
    return invoice, invoice_item


def test_create_return_with_item(db_session):
    user = _make_user(db_session)
    product = _make_product(db_session)
    invoice, invoice_item = _make_invoice_item(db_session, user, product)

    return_ = Return(invoice_number=invoice.invoice_number)
    return_.items.append(ReturnItem(invoice_item_id=invoice_item.invoice_item_id, quantity=1))
    db_session.add(return_)
    db_session.commit()

    assert isinstance(return_.return_id, uuid.UUID)
    assert return_.returned_at is not None
    assert return_.items[0].quantity == 1

    db_session.query(ReturnItem).filter_by(return_id=return_.return_id).delete()
    db_session.commit()
    db_session.delete(return_)
    db_session.commit()
    db_session.delete(invoice_item)
    db_session.commit()
    db_session.delete(invoice)
    db_session.commit()
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_return_item_requires_positive_quantity(db_session):
    user = _make_user(db_session)
    product = _make_product(db_session)
    invoice, invoice_item = _make_invoice_item(db_session, user, product)
    return_ = Return(invoice_number=invoice.invoice_number)
    db_session.add(return_)
    db_session.commit()

    db_session.add(ReturnItem(return_id=return_.return_id, invoice_item_id=invoice_item.invoice_item_id, quantity=0))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    db_session.delete(return_)
    db_session.commit()
    db_session.delete(invoice_item)
    db_session.commit()
    db_session.delete(invoice)
    db_session.commit()
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()
