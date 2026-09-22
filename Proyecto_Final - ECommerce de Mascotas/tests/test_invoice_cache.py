import uuid
from decimal import Decimal

import pytest

from app.models.invoice import Invoice, InvoiceItem
from app.models.product import Product
from app.models.user import User
from app.repositories.invoice_repository import InvoiceRepository
from app.services import sales_service
from app.utils.errors import NotFoundError


def _make_user(db_session):
    user = User(email=f"invoicecache-{uuid.uuid4().hex}@example.com", password_hash="hashed")
    db_session.add(user)
    db_session.commit()
    return user


def _make_invoice(db_session, user):
    product = Product(name=f"Product-{uuid.uuid4().hex}", price=Decimal("10.00"), stock=5)
    db_session.add(product)
    db_session.commit()

    invoice = Invoice(
        user_id=user.user_id,
        billing_street="Calle 1",
        billing_city="San Jose",
        billing_postal_code="10101",
        billing_country="Costa Rica",
        payment_method="SINPE",
    )
    invoice.items.append(
        InvoiceItem(product_id=product.product_id, quantity=1, price_at_purchase=product.price)
    )
    db_session.add(invoice)
    db_session.commit()
    return invoice, product


def _spy_on(monkeypatch, cls, method_name):
    original = getattr(cls, method_name)
    calls = {"count": 0}

    def wrapper(self, *args, **kwargs):
        calls["count"] += 1
        return original(self, *args, **kwargs)

    monkeypatch.setattr(cls, method_name, wrapper)
    return calls


def test_second_get_invoice_call_does_not_hit_the_repository(monkeypatch, db_session):
    user = _make_user(db_session)
    invoice, product = _make_invoice(db_session, user)
    calls = _spy_on(monkeypatch, InvoiceRepository, "get_by_number")

    first = sales_service.get_invoice(invoice.invoice_number, user.user_id, "regular_user")
    second = sales_service.get_invoice(invoice.invoice_number, user.user_id, "regular_user")

    assert calls["count"] == 1
    assert first == second

    for item in list(invoice.items):
        db_session.delete(item)
    db_session.commit()
    db_session.delete(invoice)
    db_session.commit()
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_authorization_is_still_enforced_when_served_from_cache(db_session):
    """
    Calienta el cache con la request del dueño (o de un admin), y confirma que
    un regular_user DISTINTO sigue recibiendo 404 aunque la respuesta ya esté
    cacheada — la decisión de autorización corre siempre, sin importar si el
    dato viene de cache o de la DB.
    """
    owner = _make_user(db_session)
    other_user = _make_user(db_session)
    invoice, product = _make_invoice(db_session, owner)

    # Calienta el cache (dueño).
    cached = sales_service.get_invoice(invoice.invoice_number, owner.user_id, "regular_user")
    assert cached["user_id"] == str(owner.user_id)

    # Otro regular_user, aunque la respuesta ya esté en cache, no puede verla.
    with pytest.raises(NotFoundError):
        sales_service.get_invoice(invoice.invoice_number, other_user.user_id, "regular_user")

    # El dueño y un admin sí pueden, sirviéndose del mismo cache ya caliente.
    assert sales_service.get_invoice(invoice.invoice_number, owner.user_id, "regular_user")
    assert sales_service.get_invoice(invoice.invoice_number, other_user.user_id, "admin")

    for item in list(invoice.items):
        db_session.delete(item)
    db_session.commit()
    db_session.delete(invoice)
    db_session.commit()
    db_session.delete(product)
    db_session.delete(owner)
    db_session.delete(other_user)
    db_session.commit()


def test_process_return_invalidates_the_specific_invoice_cache_key(db_session):
    user = _make_user(db_session)
    invoice, product = _make_invoice(db_session, user)

    cached_before = sales_service.get_invoice(invoice.invoice_number, user.user_id, "admin")
    assert cached_before["status"] == "completed"

    invoice_item_id = invoice.items[0].invoice_item_id
    return_ = sales_service.process_return(
        invoice.invoice_number, [{"invoice_item_id": invoice_item_id, "quantity": 1}]
    )

    cached_after = sales_service.get_invoice(invoice.invoice_number, user.user_id, "admin")
    assert cached_after["status"] == "fully_returned"

    for item in list(return_.items):
        db_session.delete(item)
    db_session.commit()
    db_session.delete(return_)
    db_session.commit()
    for item in list(invoice.items):
        db_session.delete(item)
    db_session.commit()
    db_session.delete(invoice)
    db_session.commit()
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()
