import uuid
from decimal import Decimal

from app.auth.jwt_utils import encode_token
from app.models.cart import Cart, CartItem, CartStatusEnum
from app.models.invoice import Invoice, InvoiceItem, InvoiceStatusEnum
from app.models.return_ import Return, ReturnItem
from app.models.product import Product, ProductStatusEnum
from app.models.user import User
from app.services import sales_service


def _make_user(db_session):
    user = User(email=f"salesroute-{uuid.uuid4().hex}@example.com", password_hash="hashed")
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


def _headers_for(user):
    token = encode_token(str(user.user_id), "regular_user")
    return {"Authorization": f"Bearer {token}"}


def _admin_headers_for(user):
    token = encode_token(str(user.user_id), "admin")
    return {"Authorization": f"Bearer {token}"}


VALID_CHECKOUT_BODY = {
    "billing_address": {
        "street": "Calle 123",
        "city": "San Jose",
        "postal_code": "10101",
        "country": "Costa Rica",
    },
    "payment_method": "SINPE",
}


# ---- SALE-01: POST /carts ----


def test_create_cart_happy_path(app, db_session):
    user = _make_user(db_session)
    client = app.test_client()

    response = client.post("/carts", headers=_headers_for(user))

    assert response.status_code == 201
    body = response.get_json()
    assert body["status"] == "pending"
    assert body["items"] == []

    db_session.query(Cart).filter_by(cart_id=body["cart_id"]).delete()
    db_session.commit()
    db_session.delete(user)
    db_session.commit()


def test_create_cart_without_token_returns_401(app):
    client = app.test_client()

    response = client.post("/carts")

    assert response.status_code == 401
    assert response.get_json() == {"error": "Authentication required"}


# ---- SALE-02: items ----


def test_add_item_happy_path(app, db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session)
    client = app.test_client()

    response = client.post(
        f"/carts/{cart.cart_id}/items",
        json={"product_id": str(product.product_id), "quantity": 2},
        headers=_headers_for(user),
    )

    assert response.status_code == 201
    item_id = response.get_json()["cart_item_id"]

    db_session.query(CartItem).filter_by(cart_item_id=item_id).delete()
    db_session.commit()
    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_add_item_malformed_cart_id_returns_404(app, db_session):
    user = _make_user(db_session)
    product = _make_product(db_session)
    client = app.test_client()

    response = client.post(
        "/carts/not-a-uuid/items",
        json={"product_id": str(product.product_id), "quantity": 1},
        headers=_headers_for(user),
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Cart not found"}

    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_add_item_cart_not_found_returns_404(app, db_session):
    user = _make_user(db_session)
    product = _make_product(db_session)
    client = app.test_client()

    response = client.post(
        f"/carts/{uuid.uuid4()}/items",
        json={"product_id": str(product.product_id), "quantity": 1},
        headers=_headers_for(user),
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Cart not found"}

    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_add_item_cart_of_another_user_returns_404(app, db_session):
    owner = _make_user(db_session)
    other_user = _make_user(db_session)
    cart = _make_cart(db_session, owner)
    product = _make_product(db_session)
    client = app.test_client()

    response = client.post(
        f"/carts/{cart.cart_id}/items",
        json={"product_id": str(product.product_id), "quantity": 1},
        headers=_headers_for(other_user),
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Cart not found"}

    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(owner)
    db_session.delete(other_user)
    db_session.commit()


def test_add_item_to_completed_cart_returns_409(app, db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user, status=CartStatusEnum.completed)
    product = _make_product(db_session)
    client = app.test_client()

    response = client.post(
        f"/carts/{cart.cart_id}/items",
        json={"product_id": str(product.product_id), "quantity": 1},
        headers=_headers_for(user),
    )

    assert response.status_code == 409
    assert response.get_json() == {"error": "Cannot modify a completed cart"}

    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_add_item_product_not_found_returns_404(app, db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    client = app.test_client()

    response = client.post(
        f"/carts/{cart.cart_id}/items",
        json={"product_id": str(uuid.uuid4()), "quantity": 1},
        headers=_headers_for(user),
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Product not found"}

    db_session.delete(cart)
    db_session.delete(user)
    db_session.commit()


def test_add_inactive_product_returns_400(app, db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session, status=ProductStatusEnum.inactive)
    client = app.test_client()

    response = client.post(
        f"/carts/{cart.cart_id}/items",
        json={"product_id": str(product.product_id), "quantity": 1},
        headers=_headers_for(user),
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Cannot add an inactive product"}

    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_add_item_invalid_quantity_returns_400(app, db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session)
    client = app.test_client()

    response = client.post(
        f"/carts/{cart.cart_id}/items",
        json={"product_id": str(product.product_id), "quantity": 0},
        headers=_headers_for(user),
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Quantity must be greater than 0"}

    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_add_item_without_token_returns_401(app, db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session)
    client = app.test_client()

    response = client.post(
        f"/carts/{cart.cart_id}/items",
        json={"product_id": str(product.product_id), "quantity": 1},
    )

    assert response.status_code == 401
    assert response.get_json() == {"error": "Authentication required"}

    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_update_item_happy_path(app, db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session)
    item = CartItem(cart_id=cart.cart_id, product_id=product.product_id, quantity=1)
    db_session.add(item)
    db_session.commit()
    client = app.test_client()

    response = client.patch(
        f"/carts/{cart.cart_id}/items/{item.cart_item_id}",
        json={"quantity": 4},
        headers=_headers_for(user),
    )

    assert response.status_code == 200
    assert response.get_json()["quantity"] == 4

    db_session.delete(item)
    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_update_item_not_in_cart_returns_404(app, db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    client = app.test_client()

    response = client.patch(
        f"/carts/{cart.cart_id}/items/{uuid.uuid4()}",
        json={"quantity": 4},
        headers=_headers_for(user),
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Item not found in cart"}

    db_session.delete(cart)
    db_session.delete(user)
    db_session.commit()


def test_remove_item_happy_path(app, db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session)
    item = CartItem(cart_id=cart.cart_id, product_id=product.product_id, quantity=1)
    db_session.add(item)
    db_session.commit()
    client = app.test_client()

    response = client.delete(
        f"/carts/{cart.cart_id}/items/{item.cart_item_id}", headers=_headers_for(user)
    )

    assert response.status_code == 200
    assert db_session.query(CartItem).filter_by(cart_item_id=item.cart_item_id).first() is None

    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


# ---- SALE-03: GET /carts?status=pending ----


def test_list_carts_returns_only_own_pending_carts(app, db_session):
    user = _make_user(db_session)
    other_user = _make_user(db_session)
    pending = _make_cart(db_session, user)
    completed = _make_cart(db_session, user, status=CartStatusEnum.completed)
    other_pending = _make_cart(db_session, other_user)
    client = app.test_client()

    response = client.get("/carts?status=pending", headers=_headers_for(user))

    assert response.status_code == 200
    ids = {cart["cart_id"] for cart in response.get_json()}
    assert str(pending.cart_id) in ids
    assert str(completed.cart_id) not in ids
    assert str(other_pending.cart_id) not in ids

    db_session.delete(pending)
    db_session.delete(completed)
    db_session.delete(other_pending)
    db_session.delete(user)
    db_session.delete(other_user)
    db_session.commit()


def test_list_carts_empty_returns_empty_list(app, db_session):
    user = _make_user(db_session)
    client = app.test_client()

    response = client.get("/carts?status=pending", headers=_headers_for(user))

    assert response.status_code == 200
    assert response.get_json() == []

    db_session.delete(user)
    db_session.commit()


def test_list_carts_without_token_returns_401(app):
    client = app.test_client()

    response = client.get("/carts")

    assert response.status_code == 401
    assert response.get_json() == {"error": "Authentication required"}


# ---- SALE-04: POST /carts/{cart_id}/checkout ----


def _cleanup(db_session, invoice=None, cart=None, products=(), users=()):
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
    for user in users:
        db_session.delete(user)
    db_session.commit()


def test_checkout_happy_path(app, db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session, stock=10, price=Decimal("30.00"))
    item = CartItem(cart_id=cart.cart_id, product_id=product.product_id, quantity=2)
    db_session.add(item)
    db_session.commit()
    client = app.test_client()

    response = client.post(
        f"/carts/{cart.cart_id}/checkout", json=VALID_CHECKOUT_BODY, headers=_headers_for(user)
    )

    assert response.status_code == 201
    invoice_number = response.get_json()["invoice_number"]

    db_session.refresh(cart)
    db_session.refresh(product)
    assert cart.status == CartStatusEnum.completed
    assert product.stock == 8

    invoice = db_session.query(Invoice).filter_by(invoice_number=invoice_number).one()

    _cleanup(db_session, invoice=invoice, cart=cart, products=[product], users=[user])


def test_checkout_cart_not_found_returns_404(app, db_session):
    user = _make_user(db_session)
    client = app.test_client()

    response = client.post(
        f"/carts/{uuid.uuid4()}/checkout", json=VALID_CHECKOUT_BODY, headers=_headers_for(user)
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Cart not found"}

    db_session.delete(user)
    db_session.commit()


def test_checkout_cart_of_another_user_returns_404(app, db_session):
    owner = _make_user(db_session)
    other_user = _make_user(db_session)
    cart = _make_cart(db_session, owner)
    client = app.test_client()

    response = client.post(
        f"/carts/{cart.cart_id}/checkout",
        json=VALID_CHECKOUT_BODY,
        headers=_headers_for(other_user),
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Cart not found"}

    db_session.delete(cart)
    db_session.delete(owner)
    db_session.delete(other_user)
    db_session.commit()


def test_checkout_already_completed_returns_409(app, db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user, status=CartStatusEnum.completed)
    client = app.test_client()

    response = client.post(
        f"/carts/{cart.cart_id}/checkout", json=VALID_CHECKOUT_BODY, headers=_headers_for(user)
    )

    assert response.status_code == 409
    assert response.get_json() == {"error": "Cart already checked out"}

    db_session.delete(cart)
    db_session.delete(user)
    db_session.commit()


def test_checkout_empty_cart_returns_400(app, db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    client = app.test_client()

    response = client.post(
        f"/carts/{cart.cart_id}/checkout", json=VALID_CHECKOUT_BODY, headers=_headers_for(user)
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Cannot checkout an empty cart"}

    db_session.delete(cart)
    db_session.delete(user)
    db_session.commit()


def test_checkout_missing_billing_address_field_returns_400(app, db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session)
    item = CartItem(cart_id=cart.cart_id, product_id=product.product_id, quantity=1)
    db_session.add(item)
    db_session.commit()
    client = app.test_client()

    incomplete_body = {
        "billing_address": {"street": "Calle 123", "city": "San Jose", "postal_code": "10101"},
        "payment_method": "SINPE",
    }

    response = client.post(
        f"/carts/{cart.cart_id}/checkout", json=incomplete_body, headers=_headers_for(user)
    )

    assert response.status_code == 400
    assert "country" in response.get_json()["error"]

    db_session.delete(item)
    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_checkout_missing_payment_method_returns_400(app, db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product = _make_product(db_session)
    item = CartItem(cart_id=cart.cart_id, product_id=product.product_id, quantity=1)
    db_session.add(item)
    db_session.commit()
    client = app.test_client()

    body = {"billing_address": VALID_CHECKOUT_BODY["billing_address"]}

    response = client.post(f"/carts/{cart.cart_id}/checkout", json=body, headers=_headers_for(user))

    assert response.status_code == 400
    assert response.get_json() == {"error": "Payment method is required"}

    db_session.delete(item)
    db_session.delete(cart)
    db_session.delete(product)
    db_session.delete(user)
    db_session.commit()


def test_checkout_insufficient_stock_returns_409_and_changes_nothing(app, db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    product_ok = _make_product(db_session, stock=10)
    product_short = _make_product(db_session, stock=1)
    db_session.add(CartItem(cart_id=cart.cart_id, product_id=product_ok.product_id, quantity=2))
    db_session.add(CartItem(cart_id=cart.cart_id, product_id=product_short.product_id, quantity=5))
    db_session.commit()
    client = app.test_client()

    response = client.post(
        f"/carts/{cart.cart_id}/checkout", json=VALID_CHECKOUT_BODY, headers=_headers_for(user)
    )

    assert response.status_code == 409
    assert product_short.name in response.get_json()["error"]

    db_session.refresh(cart)
    db_session.refresh(product_ok)
    db_session.refresh(product_short)
    assert cart.status == CartStatusEnum.pending
    assert product_ok.stock == 10
    assert product_short.stock == 1

    assert db_session.query(Invoice).filter_by(user_id=user.user_id).count() == 0

    _cleanup(db_session, cart=cart, products=[product_ok, product_short], users=[user])


def test_checkout_without_token_returns_401(app, db_session):
    user = _make_user(db_session)
    cart = _make_cart(db_session, user)
    client = app.test_client()

    response = client.post(f"/carts/{cart.cart_id}/checkout", json=VALID_CHECKOUT_BODY)

    assert response.status_code == 401
    assert response.get_json() == {"error": "Authentication required"}

    db_session.delete(cart)
    db_session.delete(user)
    db_session.commit()


# ---- SALE-05: GET /invoices, GET /invoices/{invoice_number} ----


def _checkout_via_service(db_session, user, quantity=1):
    cart = _make_cart(db_session, user)
    product = _make_product(db_session)
    db_session.add(CartItem(cart_id=cart.cart_id, product_id=product.product_id, quantity=quantity))
    db_session.commit()

    invoice = sales_service.checkout(
        cart.cart_id,
        user.user_id,
        billing_street="Calle 123",
        billing_city="San Jose",
        billing_postal_code="10101",
        billing_country="Costa Rica",
        payment_method="SINPE",
    )
    return invoice, cart, product


def test_get_invoice_happy_path(app, db_session):
    user = _make_user(db_session)
    invoice, cart, product = _checkout_via_service(db_session, user)
    client = app.test_client()

    response = client.get(f"/invoices/{invoice.invoice_number}", headers=_headers_for(user))

    assert response.status_code == 200
    assert response.get_json()["invoice_number"] == str(invoice.invoice_number)

    _cleanup(db_session, invoice=invoice, cart=cart, products=[product], users=[user])


def test_get_invoice_not_found_returns_404(app, db_session):
    user = _make_user(db_session)
    client = app.test_client()

    response = client.get(f"/invoices/{uuid.uuid4()}", headers=_headers_for(user))

    assert response.status_code == 404
    assert response.get_json() == {"error": "Invoice not found"}

    db_session.delete(user)
    db_session.commit()


def test_get_invoice_of_another_user_returns_404(app, db_session):
    owner = _make_user(db_session)
    other_user = _make_user(db_session)
    invoice, cart, product = _checkout_via_service(db_session, owner)
    client = app.test_client()

    response = client.get(f"/invoices/{invoice.invoice_number}", headers=_headers_for(other_user))

    assert response.status_code == 404
    assert response.get_json() == {"error": "Invoice not found"}

    _cleanup(db_session, invoice=invoice, cart=cart, products=[product], users=[owner, other_user])


def test_get_invoice_as_admin_can_see_any_invoice(app, db_session):
    owner = _make_user(db_session)
    admin = _make_user(db_session)
    invoice, cart, product = _checkout_via_service(db_session, owner)
    client = app.test_client()

    response = client.get(f"/invoices/{invoice.invoice_number}", headers=_admin_headers_for(admin))

    assert response.status_code == 200
    assert response.get_json()["invoice_number"] == str(invoice.invoice_number)

    _cleanup(db_session, invoice=invoice, cart=cart, products=[product], users=[owner, admin])


def test_get_invoice_without_token_returns_401(app):
    client = app.test_client()

    response = client.get(f"/invoices/{uuid.uuid4()}")

    assert response.status_code == 401
    assert response.get_json() == {"error": "Authentication required"}


def test_list_invoices_regular_user_sees_only_own(app, db_session):
    user = _make_user(db_session)
    other_user = _make_user(db_session)
    invoice, cart, product = _checkout_via_service(db_session, user)
    other_invoice, other_cart, other_product = _checkout_via_service(db_session, other_user)
    client = app.test_client()

    response = client.get("/invoices", headers=_headers_for(user))

    assert response.status_code == 200
    numbers = {item["invoice_number"] for item in response.get_json()}
    assert str(invoice.invoice_number) in numbers
    assert str(other_invoice.invoice_number) not in numbers

    _cleanup(db_session, invoice=invoice, cart=cart, products=[product], users=[user])
    _cleanup(
        db_session,
        invoice=other_invoice,
        cart=other_cart,
        products=[other_product],
        users=[other_user],
    )


def test_list_invoices_admin_sees_all(app, db_session):
    user = _make_user(db_session)
    admin = _make_user(db_session)
    invoice, cart, product = _checkout_via_service(db_session, user)
    client = app.test_client()

    response = client.get("/invoices", headers=_admin_headers_for(admin))

    assert response.status_code == 200
    numbers = {item["invoice_number"] for item in response.get_json()}
    assert str(invoice.invoice_number) in numbers

    _cleanup(db_session, invoice=invoice, cart=cart, products=[product], users=[user, admin])


def test_list_invoices_without_token_returns_401(app):
    client = app.test_client()

    response = client.get("/invoices")

    assert response.status_code == 401
    assert response.get_json() == {"error": "Authentication required"}


# ---- SALE-06: POST /invoices/{invoice_number}/returns ----


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
        product = _make_product(db_session, stock=stock)
        products.append(product)
        invoice.items.append(
            InvoiceItem(product_id=product.product_id, quantity=quantity, price_at_purchase=product.price)
        )
    db_session.add(invoice)
    db_session.commit()
    return invoice, list(invoice.items), products


def test_create_return_happy_path_partial(app, db_session):
    """Requerido por el DoD: factura con 2+ productos, devolver solo uno."""
    user = _make_user(db_session)
    admin = _make_user(db_session)
    invoice, items, products = _make_invoice_with_items(db_session, user, [5, 3])
    client = app.test_client()

    response = client.post(
        f"/invoices/{invoice.invoice_number}/returns",
        json={"items": [{"invoice_item_id": str(items[0].invoice_item_id), "quantity": 2}]},
        headers=_admin_headers_for(admin),
    )

    assert response.status_code == 201
    body = response.get_json()
    assert len(body["items"]) == 1
    assert body["items"][0]["quantity"] == 2

    db_session.refresh(invoice)
    assert invoice.status == InvoiceStatusEnum.partially_returned
    db_session.refresh(products[0])
    assert products[0].stock == 22

    db_session.query(ReturnItem).filter_by(return_id=body["return_id"]).delete()
    db_session.commit()
    db_session.query(Return).filter_by(return_id=body["return_id"]).delete()
    db_session.commit()
    _cleanup(db_session, invoice=invoice, products=products, users=[user, admin])


def test_create_return_exceeds_available_returns_409(app, db_session):
    user = _make_user(db_session)
    admin = _make_user(db_session)
    invoice, items, products = _make_invoice_with_items(db_session, user, [5])
    client = app.test_client()

    response = client.post(
        f"/invoices/{invoice.invoice_number}/returns",
        json={"items": [{"invoice_item_id": str(items[0].invoice_item_id), "quantity": 6}]},
        headers=_admin_headers_for(admin),
    )

    assert response.status_code == 409
    assert "Return quantity exceeds available" in response.get_json()["error"]

    db_session.refresh(products[0])
    assert products[0].stock == 20  # sin cambios

    _cleanup(db_session, invoice=invoice, products=products, users=[user, admin])


def test_create_return_invoice_not_found_returns_404(app, db_session):
    admin = _make_user(db_session)
    client = app.test_client()

    response = client.post(
        f"/invoices/{uuid.uuid4()}/returns",
        json={"items": [{"invoice_item_id": str(uuid.uuid4()), "quantity": 1}]},
        headers=_admin_headers_for(admin),
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Invoice not found"}

    db_session.delete(admin)
    db_session.commit()


def test_create_return_item_not_in_invoice_returns_404(app, db_session):
    user = _make_user(db_session)
    admin = _make_user(db_session)
    invoice, items, products = _make_invoice_with_items(db_session, user, [5])
    client = app.test_client()

    response = client.post(
        f"/invoices/{invoice.invoice_number}/returns",
        json={"items": [{"invoice_item_id": str(uuid.uuid4()), "quantity": 1}]},
        headers=_admin_headers_for(admin),
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Invoice item not found"}

    _cleanup(db_session, invoice=invoice, products=products, users=[user, admin])


def test_create_return_invalid_quantity_returns_400(app, db_session):
    user = _make_user(db_session)
    admin = _make_user(db_session)
    invoice, items, products = _make_invoice_with_items(db_session, user, [5])
    client = app.test_client()

    response = client.post(
        f"/invoices/{invoice.invoice_number}/returns",
        json={"items": [{"invoice_item_id": str(items[0].invoice_item_id), "quantity": 0}]},
        headers=_admin_headers_for(admin),
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Return quantity must be greater than 0"}

    _cleanup(db_session, invoice=invoice, products=products, users=[user, admin])


def test_create_return_empty_items_returns_400(app, db_session):
    user = _make_user(db_session)
    admin = _make_user(db_session)
    invoice, items, products = _make_invoice_with_items(db_session, user, [5])
    client = app.test_client()

    response = client.post(
        f"/invoices/{invoice.invoice_number}/returns",
        json={"items": []},
        headers=_admin_headers_for(admin),
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "At least one return item is required"}

    _cleanup(db_session, invoice=invoice, products=products, users=[user, admin])


def test_create_return_regular_user_returns_403(app, db_session):
    user = _make_user(db_session)
    invoice, items, products = _make_invoice_with_items(db_session, user, [5])
    client = app.test_client()

    response = client.post(
        f"/invoices/{invoice.invoice_number}/returns",
        json={"items": [{"invoice_item_id": str(items[0].invoice_item_id), "quantity": 1}]},
        headers=_headers_for(user),
    )

    assert response.status_code == 403
    assert response.get_json() == {"error": "Insufficient permissions"}

    _cleanup(db_session, invoice=invoice, products=products, users=[user])


def test_create_return_without_token_returns_401(app, db_session):
    user = _make_user(db_session)
    invoice, items, products = _make_invoice_with_items(db_session, user, [5])
    client = app.test_client()

    response = client.post(
        f"/invoices/{invoice.invoice_number}/returns",
        json={"items": [{"invoice_item_id": str(items[0].invoice_item_id), "quantity": 1}]},
    )

    assert response.status_code == 401
    assert response.get_json() == {"error": "Authentication required"}

    _cleanup(db_session, invoice=invoice, products=products, users=[user])


def test_get_invoice_after_return_reflects_updated_status(app, db_session):
    """Confirma la invalidación del cache: get_invoice después de la
    devolución debe reflejar el status actualizado, no el cacheado viejo."""
    user = _make_user(db_session)
    admin = _make_user(db_session)
    invoice, items, products = _make_invoice_with_items(db_session, user, [5])
    client = app.test_client()

    # Calienta el cache con el status original.
    warm_response = client.get(f"/invoices/{invoice.invoice_number}", headers=_headers_for(user))
    assert warm_response.get_json()["status"] == "completed"

    return_response = client.post(
        f"/invoices/{invoice.invoice_number}/returns",
        json={"items": [{"invoice_item_id": str(items[0].invoice_item_id), "quantity": 5}]},
        headers=_admin_headers_for(admin),
    )

    after_response = client.get(f"/invoices/{invoice.invoice_number}", headers=_headers_for(user))
    assert after_response.get_json()["status"] == "fully_returned"

    return_id = return_response.get_json()["return_id"]
    db_session.query(ReturnItem).filter_by(return_id=return_id).delete()
    db_session.commit()
    db_session.query(Return).filter_by(return_id=return_id).delete()
    db_session.commit()
    _cleanup(db_session, invoice=invoice, products=products, users=[user, admin])
