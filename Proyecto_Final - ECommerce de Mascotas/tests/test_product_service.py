import uuid
from decimal import Decimal

import pytest

from app.models.product import Product, ProductStatusEnum
from app.services import product_service
from app.utils.errors import ConflictError, NotFoundError


def _unique_name():
    return f"Product-{uuid.uuid4().hex}"


def _make_active_product(db_session, **overrides):
    defaults = {"name": _unique_name(), "price": Decimal("10.00"), "stock": 5}
    defaults.update(overrides)
    product = Product(**defaults)
    db_session.add(product)
    db_session.commit()
    return product


def test_create_product_defaults_to_active(db_session):
    product = product_service.create_product(
        name=_unique_name(), description="desc", price=Decimal("12.50"), stock=2
    )

    assert product.status == ProductStatusEnum.active

    db_session.query(Product).filter_by(product_id=product.product_id).delete()
    db_session.commit()


def test_list_active_products_returns_only_active(db_session):
    active_product = _make_active_product(db_session)
    inactive_product = _make_active_product(db_session, status=ProductStatusEnum.inactive)

    products = product_service.list_active_products()
    ids = {product["product_id"] for product in products}

    assert str(active_product.product_id) in ids
    assert str(inactive_product.product_id) not in ids

    db_session.delete(active_product)
    db_session.delete(inactive_product)
    db_session.commit()


def test_get_product_not_found_raises():
    with pytest.raises(NotFoundError):
        product_service.get_product(uuid.uuid4(), "admin")


def test_get_product_inactive_as_regular_user_raises_not_found(db_session):
    product = _make_active_product(db_session, status=ProductStatusEnum.inactive)

    with pytest.raises(NotFoundError):
        product_service.get_product(product.product_id, "regular_user")

    db_session.delete(product)
    db_session.commit()


def test_get_product_inactive_as_admin_returns_product(db_session):
    product = _make_active_product(db_session, status=ProductStatusEnum.inactive)

    found = product_service.get_product(product.product_id, "admin")

    assert found["product_id"] == str(product.product_id)

    db_session.delete(product)
    db_session.commit()


def test_update_product_not_found_raises():
    with pytest.raises(NotFoundError):
        product_service.update_product(uuid.uuid4(), price=Decimal("5.00"))


def test_update_product_inactive_raises_conflict(db_session):
    product = _make_active_product(db_session, status=ProductStatusEnum.inactive)

    with pytest.raises(ConflictError):
        product_service.update_product(product.product_id, price=Decimal("5.00"))

    db_session.delete(product)
    db_session.commit()


def test_update_product_happy_path_updates_fields(db_session):
    product = _make_active_product(db_session)

    updated = product_service.update_product(product.product_id, price=Decimal("99.99"), stock=7)

    assert updated.price == Decimal("99.99")
    assert updated.stock == 7

    db_session.delete(product)
    db_session.commit()


def test_delete_product_not_found_raises():
    with pytest.raises(NotFoundError):
        product_service.delete_product(uuid.uuid4())


def test_delete_product_already_inactive_raises_conflict(db_session):
    product = _make_active_product(db_session, status=ProductStatusEnum.inactive)

    with pytest.raises(ConflictError):
        product_service.delete_product(product.product_id)

    db_session.delete(product)
    db_session.commit()


def test_delete_product_happy_path_sets_inactive(db_session):
    product = _make_active_product(db_session)

    deleted = product_service.delete_product(product.product_id)

    assert deleted.status == ProductStatusEnum.inactive

    db_session.delete(product)
    db_session.commit()
