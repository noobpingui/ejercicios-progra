import uuid
from decimal import Decimal

import pytest

from app.models.product import Product, ProductStatusEnum
from app.repositories.product_repository import ProductRepository
from app.services import product_service
from app.utils import cache
from app.utils.errors import NotFoundError


def _unique_name():
    return f"Product-{uuid.uuid4().hex}"


def _make_product(db_session, **overrides):
    defaults = {"name": _unique_name(), "price": Decimal("10.00"), "stock": 5}
    defaults.update(overrides)
    product = Product(**defaults)
    db_session.add(product)
    db_session.commit()
    return product


def _spy_on(monkeypatch, cls, method_name):
    original = getattr(cls, method_name)
    calls = {"count": 0}

    def wrapper(self, *args, **kwargs):
        calls["count"] += 1
        return original(self, *args, **kwargs)

    monkeypatch.setattr(cls, method_name, wrapper)
    return calls


def test_second_list_call_does_not_hit_the_repository(monkeypatch, db_session):
    product = _make_product(db_session)
    calls = _spy_on(monkeypatch, ProductRepository, "list_active")

    first = product_service.list_active_products()
    second = product_service.list_active_products()

    assert calls["count"] == 1
    assert first == second

    db_session.delete(product)
    db_session.commit()


def test_create_product_invalidates_the_list_cache(db_session):
    initial_ids = {item["product_id"] for item in product_service.list_active_products()}

    created = product_service.create_product(
        name=_unique_name(), description=None, price=Decimal("5.00"), stock=1
    )

    refreshed_ids = {item["product_id"] for item in product_service.list_active_products()}

    assert str(created.product_id) not in initial_ids
    assert str(created.product_id) in refreshed_ids

    db_session.query(Product).filter_by(product_id=created.product_id).delete()
    db_session.commit()


def test_second_get_call_for_active_product_does_not_hit_the_repository(monkeypatch, db_session):
    product = _make_product(db_session)
    calls = _spy_on(monkeypatch, ProductRepository, "get_by_id")

    first = product_service.get_product(product.product_id, "regular_user")
    second = product_service.get_product(product.product_id, "regular_user")

    assert calls["count"] == 1
    assert first == second

    db_session.delete(product)
    db_session.commit()


def test_update_product_invalidates_its_specific_cache_key(db_session):
    product = _make_product(db_session)

    cached_before = product_service.get_product(product.product_id, "regular_user")
    assert cached_before["price"] == "10.00"

    product_service.update_product(product.product_id, price=Decimal("50.00"))

    cached_after = product_service.get_product(product.product_id, "regular_user")
    assert cached_after["price"] == "50.00"

    db_session.delete(product)
    db_session.commit()


def test_delete_product_invalidates_its_specific_cache_key(db_session):
    product = _make_product(db_session)

    product_service.get_product(product.product_id, "regular_user")  # calienta el cache

    product_service.delete_product(product.product_id)

    # Ahora es inactive: regular_user debe recibir 404 (nunca la respuesta vieja cacheada).
    with pytest.raises(NotFoundError):
        product_service.get_product(product.product_id, "regular_user")

    db_session.delete(product)
    db_session.commit()


def test_inactive_product_never_touches_the_cache(monkeypatch, db_session):
    product = _make_product(db_session, status=ProductStatusEnum.inactive)

    get_calls = {"count": 0}
    set_calls = {"count": 0}

    original_get = cache.get
    original_set = cache.set

    def spy_get(key):
        get_calls["count"] += 1
        return original_get(key)

    def spy_set(key, value, ttl=None):
        set_calls["count"] += 1
        return original_set(key, value, ttl=ttl)

    monkeypatch.setattr("app.services.product_service.cache.get", spy_get)
    monkeypatch.setattr("app.services.product_service.cache.set", spy_set)

    result = product_service.get_product(product.product_id, "admin")

    assert result["status"] == "inactive"
    assert get_calls["count"] == 0
    assert set_calls["count"] == 0

    db_session.delete(product)
    db_session.commit()
