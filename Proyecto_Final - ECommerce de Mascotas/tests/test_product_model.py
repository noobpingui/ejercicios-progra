import uuid
from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.product import Product, ProductStatusEnum


def test_create_product_generates_uuid_and_defaults(db_session):
    product = Product(name="Collar", price=Decimal("10.50"), stock=5)
    db_session.add(product)
    db_session.commit()

    assert isinstance(product.product_id, uuid.UUID)
    assert product.status == ProductStatusEnum.active

    db_session.delete(product)
    db_session.commit()


def test_price_must_be_positive(db_session):
    db_session.add(Product(name="Invalid price", price=Decimal("0"), stock=1))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_stock_cannot_be_negative(db_session):
    db_session.add(Product(name="Invalid stock", price=Decimal("5"), stock=-1))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
