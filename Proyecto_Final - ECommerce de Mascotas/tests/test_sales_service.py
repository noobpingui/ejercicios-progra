import threading
import time
import uuid
from decimal import Decimal

import pytest

from app.models.cart import Cart, CartItem, CartStatusEnum
from app.models.invoice import Invoice, InvoiceItem, InvoiceStatusEnum
from app.models.product import Product, ProductStatusEnum
from app.models.user import User
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.return_repository import ReturnRepository
from app.services import sales_service
from app.utils.errors import ConflictError, NotFoundError, ValidationError


def _make_user(db_session):
    user = User(email=f"sales-{uuid.uuid4().hex}@example.com", password_hash="hashed")
    db_session.add(user)
    db_session.commit()
    return user


def _make_product(db_session, **overrides):
    defaults = {"name": f"Product-{uuid.uuid4().hex}", "price": Decimal("10.00"), "stock": 5}
    defaults.update(overrides)
    product = Product(**defaults)
    db_session.add(product)
    db_session.commit()
    return product


def _make_cart(db_session, user, **overrides):
    cart = Cart(user_id=user.user_id, **overrides)
    db_session.add(cart)
    db_session.commit()
    return cart


def _add_item(db_session, cart, product, quantity):
    item = CartItem(cart_id=cart.cart_id, product_id=product.product_id, quantity=quantity)
    db_session.add(item)
    db_session.commit()
    return item


CHECKOUT_KWARGS = {
    "billing_street": "Calle 123",
    "billing_city": "San Jose",
    "billing_postal_code": "10101",
    "billing_country": "Costa Rica",
    "payment_method": "SINPE",
}


def test_create_cart_defaults_to_pending(db_session):
    user = _make_user(db_session)

    cart = sales_service.create_cart(user.user_id)

    assert cart.status == CartStatusEnum.pending
    assert cart.user_id == user.user_id

    db_session.query(Cart).filter_by(cart_id=cart.cart_id).delete()
    db_session.commit()
    db_session.delete(user)
    db_session.commit()


def test_list_pending_carts_only_returns_owned_pending_carts(db_session):
    user = _make_user(db_session)
    other_user = _make_user(db_session)
    pending = _make_cart(db_session, user)
    completed = _make_cart(db_session, user, status=CartStatusEnum.completed)
    other_pending = _make_cart(db_session, other_user)

    carts = sales_service.list_pending_carts(user.user_id)
    ids = {cart.cart_id for cart in carts}

    assert pending.cart_id in ids
    assert completed.cart_id not in ids
    assert other_pending.cart_id not in ids

    db_session.delete(pending)
    db_session.delete(completed)
    db_session.delete(other_pending)
    db_session.delete(user)
    db_session.delete(other_user)
    db_session.commit()


def test_add_item_cart_not_found_raises(db_session):
    user = _make_user(db_session)

    with pytest.raises(NotFoundError):
        sales_service.add_item(uuid.uuid4(), user.user_id, uuid.uuid4(), 1)

    db_session.delete(user)
    db_session.commit()


def test_add_item_cart_of_another_user_raises_not_found(db_session):
    owner = _make_user(db_session)
    other_user = _make_user(db_session)
    cart = _make_cart(db_session, owner)
    product = _make_product(db_session)

    with pytest.raises(NotFoundError):
        sales_service.add_item(cart.cart_id, other_user.user_id, product.product_id, 1)

    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(owner)
    db_session.delete(other_user)
    db_session.commit()


def test_add_item_to_completed_cart_raises_conflict(db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user, status=CartStatusEnum.completed)
    product = _make_product(db_session)

    with pytest.raises(ConflictError):
        sales_service.add_item(cart.cart_id, user.user_id, product.product_id, 1)

    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_add_item_product_not_found_raises(db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)

    with pytest.raises(NotFoundError):
        sales_service.add_item(cart.cart_id, user.user_id, uuid.uuid4(), 1)

    db_session.delete(cart)
    db_session.delete(user)
    db_session.commit()


def test_add_item_inactive_product_raises_validation_error(db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session, status=ProductStatusEnum.inactive)

    with pytest.raises(ValidationError):
        sales_service.add_item(cart.cart_id, user.user_id, product.product_id, 1)

    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_add_item_happy_path(db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session)

    item = sales_service.add_item(cart.cart_id, user.user_id, product.product_id, 3)

    assert item.quantity == 3
    assert item.product_id == product.product_id

    db_session.query(CartItem).filter_by(cart_item_id=item.cart_item_id).delete()
    db_session.commit()
    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_update_item_quantity_not_in_cart_raises_not_found(db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)

    with pytest.raises(NotFoundError):
        sales_service.update_item_quantity(cart.cart_id, user.user_id, uuid.uuid4(), 5)

    db_session.delete(cart)
    db_session.delete(user)
    db_session.commit()


def test_update_item_quantity_happy_path(db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session)
    item = sales_service.add_item(cart.cart_id, user.user_id, product.product_id, 1)

    updated = sales_service.update_item_quantity(cart.cart_id, user.user_id, item.cart_item_id, 9)

    assert updated.quantity == 9

    db_session.query(CartItem).filter_by(cart_item_id=item.cart_item_id).delete()
    db_session.commit()
    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_update_item_quantity_on_completed_cart_raises_conflict(db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session)
    item = sales_service.add_item(cart.cart_id, user.user_id, product.product_id, 1)
    cart.status = CartStatusEnum.completed
    db_session.commit()

    with pytest.raises(ConflictError):
        sales_service.update_item_quantity(cart.cart_id, user.user_id, item.cart_item_id, 2)

    db_session.query(CartItem).filter_by(cart_item_id=item.cart_item_id).delete()
    db_session.commit()
    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_remove_item_not_in_cart_raises_not_found(db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)

    with pytest.raises(NotFoundError):
        sales_service.remove_item(cart.cart_id, user.user_id, uuid.uuid4())

    db_session.delete(cart)
    db_session.delete(user)
    db_session.commit()


def test_remove_item_happy_path(db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session)
    item = sales_service.add_item(cart.cart_id, user.user_id, product.product_id, 1)

    sales_service.remove_item(cart.cart_id, user.user_id, item.cart_item_id)

    assert db_session.query(CartItem).filter_by(cart_item_id=item.cart_item_id).first() is None

    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


# ---- SALE-04: checkout ----


def _cleanup_checkout(db_session, invoice=None, cart=None, products=(), user=None):
    if invoice is not None:
        for item in list(invoice.items):
            db_session.delete(item)
        db_session.commit()
        db_session.delete(invoice)
        db_session.commit()
    if cart is not None:
        db_session.delete(cart)
        db_session.commit()
    for product in products:
        db_session.delete(product)
    if user is not None:
        db_session.delete(user)
    db_session.commit()


def test_checkout_cart_not_found_raises(db_session):
    user = _make_user(db_session)

    with pytest.raises(NotFoundError):
        sales_service.checkout(uuid.uuid4(), user.user_id, **CHECKOUT_KWARGS)

    db_session.delete(user)
    db_session.commit()


def test_checkout_cart_of_another_user_raises_not_found(db_session):
    owner = _make_user(db_session)
    other_user = _make_user(db_session)
    cart = _make_cart(db_session, owner)

    with pytest.raises(NotFoundError):
        sales_service.checkout(cart.cart_id, other_user.user_id, **CHECKOUT_KWARGS)

    db_session.delete(cart)
    db_session.delete(owner)
    db_session.delete(other_user)
    db_session.commit()


def test_checkout_already_completed_cart_raises_conflict(db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user, status=CartStatusEnum.completed)

    with pytest.raises(ConflictError):
        sales_service.checkout(cart.cart_id, user.user_id, **CHECKOUT_KWARGS)

    db_session.delete(cart)
    db_session.delete(user)
    db_session.commit()


def test_checkout_empty_cart_raises_validation_error(db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)

    with pytest.raises(ValidationError):
        sales_service.checkout(cart.cart_id, user.user_id, **CHECKOUT_KWARGS)

    db_session.delete(cart)
    db_session.delete(user)
    db_session.commit()


def test_checkout_insufficient_stock_raises_conflict_and_changes_nothing(db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session, stock=2)
    _add_item(db_session, cart, product, 5)

    with pytest.raises(ConflictError):
        sales_service.checkout(cart.cart_id, user.user_id, **CHECKOUT_KWARGS)

    db_session.refresh(cart)
    db_session.refresh(product)
    assert cart.status == CartStatusEnum.pending
    assert product.stock == 2
    assert db_session.query(Invoice).filter_by(user_id=user.user_id).count() == 0

    _cleanup_checkout(db_session, cart=cart, products=[product], user=user)


def test_checkout_insufficient_stock_on_last_of_several_products_touches_nothing(db_session):
    """
    Caso de atomicidad explícitamente pedido: un carrito con VARIOS productos
    donde el ÚLTIMO no tiene stock suficiente. Confirma que NINGÚN producto
    (ni siquiera los que sí tenían stock de sobra) queda con el stock
    modificado, y que no se crea ninguna Invoice.
    """
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product_ok_1 = _make_product(db_session, stock=10)
    product_ok_2 = _make_product(db_session, stock=10)
    product_insufficient = _make_product(db_session, stock=1)
    _add_item(db_session, cart, product_ok_1, 2)
    _add_item(db_session, cart, product_ok_2, 3)
    _add_item(db_session, cart, product_insufficient, 5)  # este es el que falla

    with pytest.raises(ConflictError):
        sales_service.checkout(cart.cart_id, user.user_id, **CHECKOUT_KWARGS)

    db_session.refresh(cart)
    db_session.refresh(product_ok_1)
    db_session.refresh(product_ok_2)
    db_session.refresh(product_insufficient)

    assert cart.status == CartStatusEnum.pending
    assert product_ok_1.stock == 10
    assert product_ok_2.stock == 10
    assert product_insufficient.stock == 1
    assert db_session.query(Invoice).filter_by(user_id=user.user_id).count() == 0

    _cleanup_checkout(
        db_session,
        cart=cart,
        products=[product_ok_1, product_ok_2, product_insufficient],
        user=user,
    )


def test_checkout_same_product_in_two_lines_sums_demand_before_checking_stock(db_session):
    """
    add_item no deduplica productos repetidos en el mismo carrito. Si el mismo
    producto aparece en dos CartItem con quantity 3 cada uno y el stock es 5,
    cada línea individualmente parece alcanzar (3 <= 5), pero la demanda total
    (6) excede el stock — el checkout debe rechazar la operación completa.
    """
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session, stock=5)
    _add_item(db_session, cart, product, 3)
    _add_item(db_session, cart, product, 3)

    with pytest.raises(ConflictError):
        sales_service.checkout(cart.cart_id, user.user_id, **CHECKOUT_KWARGS)

    db_session.refresh(product)
    assert product.stock == 5

    _cleanup_checkout(db_session, cart=cart, products=[product], user=user)


def test_checkout_happy_path_creates_invoice_reduces_stock_and_completes_cart(db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session, stock=10, price=Decimal("25.00"))
    _add_item(db_session, cart, product, 4)

    invoice = sales_service.checkout(cart.cart_id, user.user_id, **CHECKOUT_KWARGS)

    assert invoice.status == InvoiceStatusEnum.completed
    assert invoice.user_id == user.user_id
    assert len(invoice.items) == 1
    assert invoice.items[0].quantity == 4
    assert invoice.items[0].price_at_purchase == Decimal("25.00")

    db_session.refresh(cart)
    db_session.refresh(product)
    assert cart.status == CartStatusEnum.completed
    assert product.stock == 6

    _cleanup_checkout(db_session, invoice=invoice, cart=cart, products=[product], user=user)


def test_checkout_price_at_purchase_is_frozen_after_product_price_changes(db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session, stock=10, price=Decimal("25.00"))
    _add_item(db_session, cart, product, 1)

    invoice = sales_service.checkout(cart.cart_id, user.user_id, **CHECKOUT_KWARGS)
    invoice_number = invoice.invoice_number

    product.price = Decimal("999.99")
    db_session.commit()

    reloaded_invoice = db_session.query(Invoice).filter_by(invoice_number=invoice_number).one()
    assert reloaded_invoice.items[0].price_at_purchase == Decimal("25.00")

    _cleanup_checkout(db_session, invoice=reloaded_invoice, cart=cart, products=[product], user=user)


# ---- SALE-05: consultar factura ----


def test_get_invoice_not_found_raises(db_session):
    user = _make_user(db_session)

    with pytest.raises(NotFoundError):
        sales_service.get_invoice(uuid.uuid4(), user.user_id, "regular_user")

    db_session.delete(user)
    db_session.commit()


def test_get_invoice_of_another_user_as_regular_user_raises_not_found(db_session):
    owner = _make_user(db_session)
    other_user = _make_user(db_session)
    cart = _make_cart(db_session, owner)
    product = _make_product(db_session)
    _add_item(db_session, cart, product, 1)
    invoice = sales_service.checkout(cart.cart_id, owner.user_id, **CHECKOUT_KWARGS)

    with pytest.raises(NotFoundError):
        sales_service.get_invoice(invoice.invoice_number, other_user.user_id, "regular_user")

    _cleanup_checkout(db_session, invoice=invoice, cart=cart, products=[product], user=owner)
    db_session.delete(other_user)
    db_session.commit()


def test_get_invoice_as_admin_can_see_any_invoice(db_session):
    owner = _make_user(db_session)
    admin = _make_user(db_session)
    cart = _make_cart(db_session, owner)
    product = _make_product(db_session)
    _add_item(db_session, cart, product, 1)
    invoice = sales_service.checkout(cart.cart_id, owner.user_id, **CHECKOUT_KWARGS)

    found = sales_service.get_invoice(invoice.invoice_number, admin.user_id, "admin")
    assert found["invoice_number"] == str(invoice.invoice_number)

    _cleanup_checkout(db_session, invoice=invoice, cart=cart, products=[product], user=owner)
    db_session.delete(admin)
    db_session.commit()


def test_list_invoices_regular_user_sees_only_own(db_session):
    user = _make_user(db_session)
    other_user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    other_cart = _make_cart(db_session, other_user)
    product = _make_product(db_session)
    other_product = _make_product(db_session)
    _add_item(db_session, cart, product, 1)
    _add_item(db_session, other_cart, other_product, 1)
    invoice = sales_service.checkout(cart.cart_id, user.user_id, **CHECKOUT_KWARGS)
    other_invoice = sales_service.checkout(other_cart.cart_id, other_user.user_id, **CHECKOUT_KWARGS)

    invoices = sales_service.list_invoices(user.user_id, "regular_user")
    numbers = {item["invoice_number"] for item in invoices}

    assert str(invoice.invoice_number) in numbers
    assert str(other_invoice.invoice_number) not in numbers

    _cleanup_checkout(db_session, invoice=invoice, cart=cart, products=[product], user=user)
    _cleanup_checkout(
        db_session, invoice=other_invoice, cart=other_cart, products=[other_product], user=other_user
    )


def test_list_invoices_admin_sees_all(db_session):
    user = _make_user(db_session)
    admin = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session)
    _add_item(db_session, cart, product, 1)
    invoice = sales_service.checkout(cart.cart_id, user.user_id, **CHECKOUT_KWARGS)

    invoices = sales_service.list_invoices(admin.user_id, "admin")
    numbers = {item["invoice_number"] for item in invoices}

    assert str(invoice.invoice_number) in numbers

    _cleanup_checkout(db_session, invoice=invoice, cart=cart, products=[product], user=user)
    db_session.delete(admin)
    db_session.commit()


# ---- Concurrencia: dos checkouts reales compitiendo por el mismo producto ----


def test_concurrent_checkouts_on_shared_product_are_serialized_by_row_lock(db_session, monkeypatch):
    """
    Dos carritos de dos usuarios distintos piden 3 unidades cada uno de un
    producto con stock=5 (5 no alcanza para ambos: 3+3=6). Sin el lock de fila
    (SELECT ... FOR UPDATE), ambos threads podrían leer stock=5 "al mismo
    tiempo" y los dos concluir que hay suficiente, sobrevendiendo el producto.

    Para que el test sea determinístico (no dependiente de timing real) se
    instrumenta ProductRepository.get_for_update: el primer thread que llega
    ahí queda retenido (ya con el lock de Postgres tomado, transacción abierta
    sin commit) hasta que el segundo thread efectivamente intente tomar el
    mismo lock y quede bloqueado esperando en la DB. Solo entonces se libera
    al primero, confirmando que el segundo lo esperó de verdad — no que
    simplemente corrió después por casualidad de scheduling.
    """
    user_1 = _make_user(db_session)
    user_2 = _make_user(db_session)
    product = _make_product(db_session, stock=5)
    cart_1 = _make_cart(db_session, user_1)
    cart_2 = _make_cart(db_session, user_2)
    _add_item(db_session, cart_1, product, 3)
    _add_item(db_session, cart_2, product, 3)

    original_get_for_update = ProductRepository.get_for_update

    first_caller_id = {"thread_ident": None}
    first_caller_locked = threading.Event()
    release_first_caller = threading.Event()

    def instrumented_get_for_update(self, product_id):
        # Esta llamada ya ejecutó el SELECT ... FOR UPDATE contra Postgres —
        # el lock de fila ya está tomado en este punto (o esta misma línea
        # bloqueó esperando el lock, si otro thread lo tenía).
        result = original_get_for_update(self, product_id)

        current_ident = threading.get_ident()
        if first_caller_id["thread_ident"] is None:
            first_caller_id["thread_ident"] = current_ident
            first_caller_locked.set()
            # Retenemos el lock (transacción sin commit) hasta confirmar que
            # el otro thread quedó esperando por él.
            release_first_caller.wait(timeout=5)

        return result

    monkeypatch.setattr(ProductRepository, "get_for_update", instrumented_get_for_update)

    results = {}

    def run_checkout(cart, user, key):
        try:
            invoice = sales_service.checkout(cart.cart_id, user.user_id, **CHECKOUT_KWARGS)
            results[key] = ("success", invoice)
        except ConflictError as exc:
            results[key] = ("conflict", str(exc))
        except Exception as exc:  # noqa: BLE001 - queremos ver cualquier falla inesperada del thread
            results[key] = ("error", exc)

    thread_a = threading.Thread(target=run_checkout, args=(cart_1, user_1, "a"))
    thread_b = threading.Thread(target=run_checkout, args=(cart_2, user_2, "b"))

    thread_a.start()
    assert first_caller_locked.wait(timeout=5), "thread_a nunca llegó a tomar el lock"

    thread_b.start()
    # Le damos tiempo real a thread_b para que llegue al FOR UPDATE y quede
    # efectivamente bloqueado esperando el lock que tiene thread_a.
    time.sleep(0.5)
    assert thread_b.is_alive(), "thread_b no debería poder avanzar mientras thread_a tiene el lock"

    release_first_caller.set()

    thread_a.join(timeout=10)
    thread_b.join(timeout=10)

    assert not thread_a.is_alive(), "thread_a no terminó a tiempo"
    assert not thread_b.is_alive(), "thread_b no terminó a tiempo"

    # thread_a fue, por construcción del test, el único que pudo tomar el lock
    # primero (thread_b ni siquiera arrancó hasta que thread_a ya lo tenía) —
    # así que thread_a es determinísticamente el que gana el checkout.
    assert results["a"][0] == "success", results
    assert results["b"][0] == "conflict", results
    # thread_b vio el stock YA actualizado por thread_a (2, no el 5 original)
    # — por eso el mensaje de "insuficiente", no una condición de carrera
    # silenciosa que hubiera dejado pasar ambos checkouts.
    assert "Insufficient stock" in results["b"][1]

    db_session.refresh(product)
    assert product.stock == 2  # 5 - 3 (una sola reducción aplicada, nunca las dos)
    assert product.stock >= 0

    # cart_2 (el que perdió) sigue con su CartItem apuntando al producto — hay
    # que borrarlo ANTES de borrar el producto, o la FK lo bloquea. Se hace en
    # commits separados porque no hay relación ORM cart<->user que le permita
    # a SQLAlchemy resolver solo el orden de borrado entre las dos tablas.
    db_session.delete(cart_2)
    db_session.commit()
    db_session.delete(user_2)
    db_session.commit()

    winner_invoice = results["a"][1]
    _cleanup_checkout(
        db_session, invoice=winner_invoice, cart=cart_1, products=[product], user=user_1
    )


# ---- SALE-06: procesar devolución ----


def _make_invoice_with_items(db_session, user, quantities, stock=20):
    products = []
    invoice = Invoice(
        user_id=user.user_id,
        billing_street="Calle 1",
        billing_city="San Jose",
        billing_postal_code="10101",
        billing_country="Costa Rica",
        payment_method="SINPE",
    )
    for quantity in quantities:
        product = Product(name=f"Product-{uuid.uuid4().hex}", price=Decimal("10.00"), stock=stock)
        db_session.add(product)
        db_session.flush()
        products.append(product)
        invoice.items.append(
            InvoiceItem(product_id=product.product_id, quantity=quantity, price_at_purchase=product.price)
        )
    db_session.add(invoice)
    db_session.commit()
    return invoice, list(invoice.items), products


def _cleanup_return(db_session, return_=None, invoice=None, products=(), user=None):
    if return_ is not None:
        for item in list(return_.items):
            db_session.delete(item)
        db_session.commit()
        db_session.delete(return_)
        db_session.commit()
    if invoice is not None:
        for item in list(invoice.items):
            db_session.delete(item)
        db_session.commit()
        db_session.delete(invoice)
        db_session.commit()
    for product in products:
        db_session.delete(product)
    if user is not None:
        db_session.delete(user)
    db_session.commit()


def test_process_return_invoice_not_found_raises():
    with pytest.raises(NotFoundError):
        sales_service.process_return(uuid.uuid4(), [{"invoice_item_id": uuid.uuid4(), "quantity": 1}])


def test_process_return_item_not_found_raises(db_session):
    user = _make_user(db_session)
    invoice, items, products = _make_invoice_with_items(db_session, user, [5])

    with pytest.raises(NotFoundError):
        sales_service.process_return(
            invoice.invoice_number, [{"invoice_item_id": uuid.uuid4(), "quantity": 1}]
        )

    _cleanup_return(db_session, invoice=invoice, products=products, user=user)


def test_process_return_item_from_another_invoice_raises_not_found(db_session):
    user = _make_user(db_session)
    invoice_1, items_1, products_1 = _make_invoice_with_items(db_session, user, [5])
    invoice_2, items_2, products_2 = _make_invoice_with_items(db_session, user, [5])

    with pytest.raises(NotFoundError):
        sales_service.process_return(
            invoice_1.invoice_number,
            [{"invoice_item_id": items_2[0].invoice_item_id, "quantity": 1}],
        )

    _cleanup_return(db_session, invoice=invoice_1, products=products_1, user=None)
    _cleanup_return(db_session, invoice=invoice_2, products=products_2, user=user)


def test_process_return_exceeds_available_raises_conflict(db_session):
    user = _make_user(db_session)
    invoice, items, products = _make_invoice_with_items(db_session, user, [5])

    with pytest.raises(ConflictError):
        sales_service.process_return(
            invoice.invoice_number,
            [{"invoice_item_id": items[0].invoice_item_id, "quantity": 6}],
        )

    _cleanup_return(db_session, invoice=invoice, products=products, user=user)


def test_process_return_exceeds_available_accounts_for_previous_returns(db_session):
    user = _make_user(db_session)
    invoice, items, products = _make_invoice_with_items(db_session, user, [5])

    first_return = sales_service.process_return(
        invoice.invoice_number, [{"invoice_item_id": items[0].invoice_item_id, "quantity": 3}]
    )

    with pytest.raises(ConflictError):
        sales_service.process_return(
            invoice.invoice_number,
            [{"invoice_item_id": items[0].invoice_item_id, "quantity": 3}],  # solo quedan 2
        )

    _cleanup_return(db_session, return_=first_return)
    _cleanup_return(db_session, invoice=invoice, products=products, user=user)


def test_process_return_partial_return_of_one_of_several_items(db_session):
    """
    Requerido explícitamente por el DoD: factura con 2+ productos, devolver
    solo uno (parcialmente) — confirma devolución parcial real.
    """
    user = _make_user(db_session)
    invoice, items, products = _make_invoice_with_items(db_session, user, [5, 3])

    return_ = sales_service.process_return(
        invoice.invoice_number, [{"invoice_item_id": items[0].invoice_item_id, "quantity": 2}]
    )

    assert len(return_.items) == 1
    assert return_.items[0].quantity == 2

    db_session.refresh(invoice)
    assert invoice.status == InvoiceStatusEnum.partially_returned

    db_session.refresh(products[0])
    db_session.refresh(products[1])
    assert products[0].stock == 22  # 20 + 2 restaurados
    assert products[1].stock == 20  # sin cambios, no se tocó ese ítem

    _cleanup_return(db_session, return_=return_)
    _cleanup_return(db_session, invoice=invoice, products=products, user=user)


def test_process_return_full_return_of_all_items_sets_fully_returned(db_session):
    user = _make_user(db_session)
    invoice, items, products = _make_invoice_with_items(db_session, user, [5, 3])

    return_ = sales_service.process_return(
        invoice.invoice_number,
        [
            {"invoice_item_id": items[0].invoice_item_id, "quantity": 5},
            {"invoice_item_id": items[1].invoice_item_id, "quantity": 3},
        ],
    )

    db_session.refresh(invoice)
    assert invoice.status == InvoiceStatusEnum.fully_returned

    _cleanup_return(db_session, return_=return_)
    _cleanup_return(db_session, invoice=invoice, products=products, user=user)


def test_process_return_second_partial_return_completes_to_fully_returned(db_session):
    user = _make_user(db_session)
    invoice, items, products = _make_invoice_with_items(db_session, user, [5])

    first_return = sales_service.process_return(
        invoice.invoice_number, [{"invoice_item_id": items[0].invoice_item_id, "quantity": 2}]
    )
    db_session.refresh(invoice)
    assert invoice.status == InvoiceStatusEnum.partially_returned

    second_return = sales_service.process_return(
        invoice.invoice_number, [{"invoice_item_id": items[0].invoice_item_id, "quantity": 3}]
    )
    db_session.refresh(invoice)
    assert invoice.status == InvoiceStatusEnum.fully_returned

    _cleanup_return(db_session, return_=first_return)
    _cleanup_return(db_session, return_=second_return)
    _cleanup_return(db_session, invoice=invoice, products=products, user=user)


def test_process_return_invalidates_invoice_cache(db_session):
    user = _make_user(db_session)
    invoice, items, products = _make_invoice_with_items(db_session, user, [5])

    cached_before = sales_service.get_invoice(invoice.invoice_number, user.user_id, "admin")
    assert cached_before["status"] == "completed"

    return_ = sales_service.process_return(
        invoice.invoice_number, [{"invoice_item_id": items[0].invoice_item_id, "quantity": 5}]
    )

    cached_after = sales_service.get_invoice(invoice.invoice_number, user.user_id, "admin")
    assert cached_after["status"] == "fully_returned"

    _cleanup_return(db_session, return_=return_)
    _cleanup_return(db_session, invoice=invoice, products=products, user=user)


def test_concurrent_returns_on_same_invoice_item_are_serialized_by_row_lock(db_session, monkeypatch):
    """
    Dos devoluciones concurrentes sobre la MISMA línea de factura (quantity
    comprada = 5), cada una pidiendo 3 unidades (3+3=6 > 5 disponible). Mismo
    riesgo de TOCTOU que en checkout, mismo patrón de instrumentación
    determinística para probarlo de verdad (no solo el resultado final).
    """
    user = _make_user(db_session)
    invoice, items, products = _make_invoice_with_items(db_session, user, [5])
    invoice_item_id = items[0].invoice_item_id

    original_get_item_for_update = InvoiceRepository.get_item_for_update

    first_caller_locked = threading.Event()
    release_first_caller = threading.Event()
    first_caller_id = {"thread_ident": None}

    def instrumented_get_item_for_update(self, invoice_number, item_id):
        result = original_get_item_for_update(self, invoice_number, item_id)

        current_ident = threading.get_ident()
        if first_caller_id["thread_ident"] is None:
            first_caller_id["thread_ident"] = current_ident
            first_caller_locked.set()
            release_first_caller.wait(timeout=5)

        return result

    monkeypatch.setattr(InvoiceRepository, "get_item_for_update", instrumented_get_item_for_update)

    results = {}

    def run_return(key):
        try:
            return_ = sales_service.process_return(
                invoice.invoice_number, [{"invoice_item_id": invoice_item_id, "quantity": 3}]
            )
            results[key] = ("success", return_)
        except ConflictError as exc:
            results[key] = ("conflict", str(exc))
        except Exception as exc:  # noqa: BLE001
            results[key] = ("error", exc)

    thread_a = threading.Thread(target=run_return, args=("a",))
    thread_b = threading.Thread(target=run_return, args=("b",))

    thread_a.start()
    assert first_caller_locked.wait(timeout=5), "thread_a nunca llegó a tomar el lock"

    thread_b.start()
    time.sleep(0.5)
    assert thread_b.is_alive(), "thread_b no debería poder avanzar mientras thread_a tiene el lock"

    release_first_caller.set()

    thread_a.join(timeout=10)
    thread_b.join(timeout=10)

    assert not thread_a.is_alive()
    assert not thread_b.is_alive()

    assert results["a"][0] == "success", results
    assert results["b"][0] == "conflict", results
    assert "Return quantity exceeds available" in results["b"][1]

    db_session.refresh(items[0])
    assert ReturnRepository(db_session).get_total_returned_quantity(invoice_item_id) == 3

    db_session.refresh(products[0])
    assert products[0].stock == 23  # 20 + 3 (una sola restauración aplicada)

    _cleanup_return(db_session, return_=results["a"][1])
    _cleanup_return(db_session, invoice=invoice, products=products, user=user)
