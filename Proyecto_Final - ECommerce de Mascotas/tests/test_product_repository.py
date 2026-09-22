import uuid
from decimal import Decimal

from app.models.product import Product, ProductStatusEnum
from app.repositories.product_repository import ProductRepository


def _unique_name():
    return f"Product-{uuid.uuid4().hex}"


def test_create_adds_product_to_session_without_committing(db_session):
    repo = ProductRepository(db_session)
    name = _unique_name()

    product = repo.create(name=name, description="desc", price=Decimal("9.99"), stock=3)

    assert product in db_session.new

    db_session.commit()

    assert isinstance(product.product_id, uuid.UUID)
    assert product.status == ProductStatusEnum.active

    db_session.delete(product)
    db_session.commit()


def test_get_by_id_found_and_not_found(db_session):
    repo = ProductRepository(db_session)
    product = repo.create(name=_unique_name(), description=None, price=Decimal("5.00"), stock=1)
    db_session.commit()

    found = repo.get_by_id(product.product_id)
    assert found is not None
    assert found.product_id == product.product_id

    assert repo.get_by_id(uuid.uuid4()) is None

    db_session.delete(product)
    db_session.commit()


def test_list_active_excludes_inactive_products(db_session):
    repo = ProductRepository(db_session)
    active_product = repo.create(name=_unique_name(), description=None, price=Decimal("5.00"), stock=1)
    inactive_product = Product(
        name=_unique_name(), price=Decimal("5.00"), stock=1, status=ProductStatusEnum.inactive
    )
    db_session.add(inactive_product)
    db_session.commit()

    active_ids = {product.product_id for product in repo.list_active()}

    assert active_product.product_id in active_ids
    assert inactive_product.product_id not in active_ids

    db_session.delete(active_product)
    db_session.delete(inactive_product)
    db_session.commit()
