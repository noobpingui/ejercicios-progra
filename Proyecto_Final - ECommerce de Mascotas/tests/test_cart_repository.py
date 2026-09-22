import uuid
from decimal import Decimal

from app.models.cart import Cart, CartStatusEnum
from app.models.product import Product
from app.models.user import User
from app.repositories.cart_repository import CartRepository


def _make_user(db_session):
    user = User(email=f"cartrepo-{uuid.uuid4().hex}@example.com", password_hash="hashed")
    db_session.add(user)
    db_session.commit()
    return user


def _make_product(db_session):
    product = Product(name=f"Product-{uuid.uuid4().hex}", price=Decimal("10.00"), stock=5)
    db_session.add(product)
    db_session.commit()
    return product


def test_create_adds_cart_without_committing(db_session):
    user = _make_user(db_session)
    repo = CartRepository(db_session)

    cart = repo.create(user.user_id)

    assert cart in db_session.new

    db_session.commit()
    assert cart.status == CartStatusEnum.pending

    db_session.delete(cart)
    db_session.delete(user)
    db_session.commit()


def test_get_owned_cart_returns_none_when_cart_does_not_exist(db_session):
    user = _make_user(db_session)
    repo = CartRepository(db_session)

    assert repo.get_owned_cart(uuid.uuid4(), user.user_id) is None

    db_session.delete(user)
    db_session.commit()


def test_get_owned_cart_returns_none_when_owned_by_another_user(db_session):
    owner = _make_user(db_session)
    other_user = _make_user(db_session)
    repo = CartRepository(db_session)
    cart = repo.create(owner.user_id)
    db_session.commit()

    assert repo.get_owned_cart(cart.cart_id, other_user.user_id) is None
    assert repo.get_owned_cart(cart.cart_id, owner.user_id) is not None

    db_session.delete(cart)
    db_session.delete(owner)
    db_session.delete(other_user)
    db_session.commit()


def test_add_update_remove_item(db_session):
    user = _make_user(db_session)
    product = _make_product(db_session)
    repo = CartRepository(db_session)
    cart = repo.create(user.user_id)
    db_session.commit()

    item = repo.add_item(cart.cart_id, product.product_id, 2)
    db_session.commit()
    assert repo.get_item(cart.cart_id, item.cart_item_id) is not None

    repo.update_item_quantity(item, 5)
    db_session.commit()
    assert item.quantity == 5

    repo.remove_item(item)
    db_session.commit()
    assert repo.get_item(cart.cart_id, item.cart_item_id) is None

    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_list_pending_by_user_excludes_other_users_and_completed_carts(db_session):
    user = _make_user(db_session)
    repo = CartRepository(db_session)
    pending_cart = repo.create(user.user_id)
    completed_cart = Cart(user_id=user.user_id, status=CartStatusEnum.completed)
    db_session.add(completed_cart)
    db_session.commit()

    result_ids = {cart.cart_id for cart in repo.list_pending_by_user(user.user_id)}

    assert pending_cart.cart_id in result_ids
    assert completed_cart.cart_id not in result_ids

    db_session.delete(pending_cart)
    db_session.delete(completed_cart)
    db_session.delete(user)
    db_session.commit()
