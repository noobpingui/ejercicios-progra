import uuid
from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.cart import Cart, CartItem, CartStatusEnum
from app.models.product import Product
from app.models.user import RoleEnum, StatusEnum, User


def _make_user(db_session):
    user = User(email=f"cart-{uuid.uuid4().hex}@example.com", password_hash="hashed")
    db_session.add(user)
    db_session.commit()
    return user


def _make_product(db_session):
    product = Product(name="Correa", price=Decimal("12.00"), stock=10)
    db_session.add(product)
    db_session.commit()
    return product


def test_create_cart_defaults_to_pending(db_session):
    user = _make_user(db_session)

    cart = Cart(user_id=user.user_id)
    db_session.add(cart)
    db_session.commit()

    assert isinstance(cart.cart_id, uuid.UUID)
    assert cart.status == CartStatusEnum.pending

    db_session.delete(cart)
    db_session.delete(user)
    db_session.commit()


def test_cart_item_requires_positive_quantity(db_session):
    user = _make_user(db_session)
    product = _make_product(db_session)
    cart = Cart(user_id=user.user_id)
    db_session.add(cart)
    db_session.commit()

    db_session.add(CartItem(cart_id=cart.cart_id, product_id=product.product_id, quantity=0))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_deleting_cart_cascades_to_its_items(db_session):
    user = _make_user(db_session)
    product = _make_product(db_session)
    cart = Cart(user_id=user.user_id)
    cart.items.append(CartItem(product_id=product.product_id, quantity=2))
    db_session.add(cart)
    db_session.commit()
    cart_item_id = cart.items[0].cart_item_id

    db_session.delete(cart)
    db_session.commit()

    assert db_session.query(CartItem).filter_by(cart_item_id=cart_item_id).first() is None

    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()
