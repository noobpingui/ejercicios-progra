import uuid
from decimal import Decimal

from app.models.invoice import Invoice, InvoiceItem
from app.models.product import Product
from app.models.user import User
from app.repositories.return_repository import ReturnRepository


def _make_user(db_session):
    user = User(email=f"returnrepo-{uuid.uuid4().hex}@example.com", password_hash="hashed")
    db_session.add(user)
    db_session.commit()
    return user


def _make_invoice_item(db_session, user, quantity=5):
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
    invoice_item = InvoiceItem(
        product_id=product.product_id, quantity=quantity, price_at_purchase=product.price
    )
    invoice.items.append(invoice_item)
    db_session.add(invoice)
    db_session.commit()
    return invoice, invoice_item, product


def test_create_and_add_item_without_committing(db_session):
    user = _make_user(db_session)
    invoice, invoice_item, product = _make_invoice_item(db_session, user)
    repo = ReturnRepository(db_session)

    return_ = repo.create(invoice_number=invoice.invoice_number)
    assert return_ in db_session.new

    repo.add_item(return_, invoice_item_id=invoice_item.invoice_item_id, quantity=2)
    db_session.commit()

    assert len(return_.items) == 1
    assert return_.items[0].quantity == 2

    db_session.delete(return_.items[0])
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


def test_get_total_returned_quantity_sums_across_multiple_returns(db_session):
    user = _make_user(db_session)
    invoice, invoice_item, product = _make_invoice_item(db_session, user, quantity=10)
    repo = ReturnRepository(db_session)

    assert repo.get_total_returned_quantity(invoice_item.invoice_item_id) == 0

    return_1 = repo.create(invoice_number=invoice.invoice_number)
    repo.add_item(return_1, invoice_item_id=invoice_item.invoice_item_id, quantity=3)
    db_session.commit()

    assert repo.get_total_returned_quantity(invoice_item.invoice_item_id) == 3

    return_2 = repo.create(invoice_number=invoice.invoice_number)
    repo.add_item(return_2, invoice_item_id=invoice_item.invoice_item_id, quantity=2)
    db_session.commit()

    assert repo.get_total_returned_quantity(invoice_item.invoice_item_id) == 5

    db_session.delete(return_1.items[0])
    db_session.delete(return_2.items[0])
    db_session.commit()
    db_session.delete(return_1)
    db_session.delete(return_2)
    db_session.commit()
    db_session.delete(invoice_item)
    db_session.commit()
    db_session.delete(invoice)
    db_session.commit()
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()
