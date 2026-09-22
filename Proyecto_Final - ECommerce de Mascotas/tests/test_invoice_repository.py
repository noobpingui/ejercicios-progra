import uuid
from decimal import Decimal

from app.models.product import Product
from app.models.user import User
from app.repositories.invoice_repository import InvoiceRepository


def _make_user(db_session):
    user = User(email=f"invoicerepo-{uuid.uuid4().hex}@example.com", password_hash="hashed")
    db_session.add(user)
    db_session.commit()
    return user


def _make_product(db_session):
    product = Product(name=f"Product-{uuid.uuid4().hex}", price=Decimal("5.00"), stock=5)
    db_session.add(product)
    db_session.commit()
    return product


def _make_invoice(repo, user):
    return repo.create(
        user_id=user.user_id,
        billing_street="Calle 1",
        billing_city="San Jose",
        billing_postal_code="10101",
        billing_country="Costa Rica",
        payment_method="SINPE",
    )


def test_create_and_add_item_without_committing(db_session):
    user = _make_user(db_session)
    product = _make_product(db_session)
    repo = InvoiceRepository(db_session)
    invoice = _make_invoice(repo, user)

    assert invoice in db_session.new

    repo.add_item(
        invoice, product_id=product.product_id, quantity=1, price_at_purchase=Decimal("5.00")
    )

    db_session.commit()
    assert len(invoice.items) == 1

    db_session.delete(invoice.items[0])
    db_session.commit()
    db_session.delete(invoice)
    db_session.commit()
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_get_by_number_found_and_not_found(db_session):
    user = _make_user(db_session)
    repo = InvoiceRepository(db_session)
    invoice = _make_invoice(repo, user)
    db_session.commit()

    found = repo.get_by_number(invoice.invoice_number)
    assert found is not None
    assert found.invoice_number == invoice.invoice_number

    assert repo.get_by_number(uuid.uuid4()) is None

    db_session.delete(invoice)
    db_session.delete(user)
    db_session.commit()


def test_list_by_user_and_list_all(db_session):
    user = _make_user(db_session)
    other_user = _make_user(db_session)
    repo = InvoiceRepository(db_session)
    invoice = _make_invoice(repo, user)
    other_invoice = _make_invoice(repo, other_user)
    db_session.commit()

    own = {i.invoice_number for i in repo.list_by_user(user.user_id)}
    assert invoice.invoice_number in own
    assert other_invoice.invoice_number not in own

    everything = {i.invoice_number for i in repo.list_all()}
    assert invoice.invoice_number in everything
    assert other_invoice.invoice_number in everything

    db_session.delete(invoice)
    db_session.delete(other_invoice)
    db_session.delete(user)
    db_session.delete(other_user)
    db_session.commit()
