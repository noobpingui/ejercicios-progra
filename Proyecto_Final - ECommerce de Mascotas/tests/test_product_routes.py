import uuid
from decimal import Decimal

from app.auth.jwt_utils import encode_token
from app.models.product import Product, ProductStatusEnum


def _unique_name():
    return f"Product-{uuid.uuid4().hex}"


def _admin_headers():
    token = encode_token(str(uuid.uuid4()), "admin")
    return {"Authorization": f"Bearer {token}"}


def _regular_user_headers():
    token = encode_token(str(uuid.uuid4()), "regular_user")
    return {"Authorization": f"Bearer {token}"}


def _make_product(db_session, **overrides):
    defaults = {"name": _unique_name(), "price": Decimal("10.00"), "stock": 5}
    defaults.update(overrides)
    product = Product(**defaults)
    db_session.add(product)
    db_session.commit()
    return product


# ---- PROD-01: POST /products ----


def test_create_product_happy_path(app, db_session):
    client = app.test_client()

    response = client.post(
        "/products",
        json={"name": _unique_name(), "price": 15.5, "stock": 3},
        headers=_admin_headers(),
    )

    assert response.status_code == 201
    product_id = response.get_json()["product_id"]

    db_session.query(Product).filter_by(product_id=product_id).delete()
    db_session.commit()


def test_create_product_missing_field_returns_400(app):
    client = app.test_client()

    response = client.post(
        "/products",
        json={"name": _unique_name(), "stock": 3},
        headers=_admin_headers(),
    )

    assert response.status_code == 400
    assert "price" in response.get_json()["error"]


def test_create_product_invalid_price_returns_400(app):
    client = app.test_client()

    response = client.post(
        "/products",
        json={"name": _unique_name(), "price": 0, "stock": 3},
        headers=_admin_headers(),
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Price must be greater than 0"}


def test_create_product_invalid_stock_returns_400(app):
    client = app.test_client()

    response = client.post(
        "/products",
        json={"name": _unique_name(), "price": 10, "stock": -1},
        headers=_admin_headers(),
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Stock cannot be negative"}


def test_create_product_regular_user_returns_403(app):
    client = app.test_client()

    response = client.post(
        "/products",
        json={"name": _unique_name(), "price": 10, "stock": 3},
        headers=_regular_user_headers(),
    )

    assert response.status_code == 403
    assert response.get_json() == {"error": "Insufficient permissions"}


def test_create_product_without_token_returns_401(app):
    client = app.test_client()

    response = client.post("/products", json={"name": _unique_name(), "price": 10, "stock": 3})

    assert response.status_code == 401
    assert response.get_json() == {"error": "Authentication required"}


# ---- PROD-02: GET /products, GET /products/{id} ----


def test_list_products_returns_only_active(app, db_session):
    active_product = _make_product(db_session)
    inactive_product = _make_product(db_session, status=ProductStatusEnum.inactive)
    client = app.test_client()

    response = client.get("/products", headers=_regular_user_headers())

    assert response.status_code == 200
    returned_ids = {item["product_id"] for item in response.get_json()}
    assert str(active_product.product_id) in returned_ids
    assert str(inactive_product.product_id) not in returned_ids

    db_session.delete(active_product)
    db_session.delete(inactive_product)
    db_session.commit()


def test_get_product_happy_path(app, db_session):
    product = _make_product(db_session)
    client = app.test_client()

    response = client.get(f"/products/{product.product_id}", headers=_regular_user_headers())

    assert response.status_code == 200
    assert response.get_json()["product_id"] == str(product.product_id)

    db_session.delete(product)
    db_session.commit()


def test_get_product_not_found_returns_404(app):
    client = app.test_client()

    response = client.get(f"/products/{uuid.uuid4()}", headers=_regular_user_headers())

    assert response.status_code == 404
    assert response.get_json() == {"error": "Product not found"}


def test_get_product_malformed_id_returns_404(app):
    client = app.test_client()

    response = client.get("/products/not-a-uuid", headers=_regular_user_headers())

    assert response.status_code == 404
    assert response.get_json() == {"error": "Product not found"}


def test_get_inactive_product_as_regular_user_returns_404(app, db_session):
    product = _make_product(db_session, status=ProductStatusEnum.inactive)
    client = app.test_client()

    response = client.get(f"/products/{product.product_id}", headers=_regular_user_headers())

    assert response.status_code == 404
    assert response.get_json() == {"error": "Product not found"}

    db_session.delete(product)
    db_session.commit()


def test_get_inactive_product_as_admin_returns_200(app, db_session):
    product = _make_product(db_session, status=ProductStatusEnum.inactive)
    client = app.test_client()

    response = client.get(f"/products/{product.product_id}", headers=_admin_headers())

    assert response.status_code == 200
    assert response.get_json()["status"] == "inactive"

    db_session.delete(product)
    db_session.commit()


def test_get_products_without_token_returns_401(app):
    client = app.test_client()

    response = client.get("/products")

    assert response.status_code == 401
    assert response.get_json() == {"error": "Authentication required"}


# ---- PROD-03: PUT /products/{id} ----


def test_update_product_happy_path(app, db_session):
    product = _make_product(db_session)
    client = app.test_client()

    response = client.put(
        f"/products/{product.product_id}",
        json={"price": "20.00"},
        headers=_admin_headers(),
    )

    assert response.status_code == 200
    assert response.get_json()["price"] == "20.00"

    db_session.delete(product)
    db_session.commit()


def test_update_product_not_found_returns_404(app):
    client = app.test_client()

    response = client.put(
        f"/products/{uuid.uuid4()}", json={"price": 20.0}, headers=_admin_headers()
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Product not found"}


def test_update_inactive_product_returns_409(app, db_session):
    product = _make_product(db_session, status=ProductStatusEnum.inactive)
    client = app.test_client()

    response = client.put(
        f"/products/{product.product_id}", json={"price": 20.0}, headers=_admin_headers()
    )

    assert response.status_code == 409
    assert response.get_json() == {"error": "Cannot modify an inactive product"}

    db_session.delete(product)
    db_session.commit()


def test_update_product_invalid_price_returns_400(app, db_session):
    product = _make_product(db_session)
    client = app.test_client()

    response = client.put(
        f"/products/{product.product_id}", json={"price": 0}, headers=_admin_headers()
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Price must be greater than 0"}

    db_session.delete(product)
    db_session.commit()


def test_update_product_invalid_stock_returns_400(app, db_session):
    product = _make_product(db_session)
    client = app.test_client()

    response = client.put(
        f"/products/{product.product_id}", json={"stock": -1}, headers=_admin_headers()
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Stock cannot be negative"}

    db_session.delete(product)
    db_session.commit()


def test_update_product_regular_user_returns_403(app, db_session):
    product = _make_product(db_session)
    client = app.test_client()

    response = client.put(
        f"/products/{product.product_id}",
        json={"price": 20.0},
        headers=_regular_user_headers(),
    )

    assert response.status_code == 403
    assert response.get_json() == {"error": "Insufficient permissions"}

    db_session.delete(product)
    db_session.commit()


def test_update_product_without_token_returns_401(app, db_session):
    product = _make_product(db_session)
    client = app.test_client()

    response = client.put(f"/products/{product.product_id}", json={"price": 20.0})

    assert response.status_code == 401
    assert response.get_json() == {"error": "Authentication required"}

    db_session.delete(product)
    db_session.commit()


# ---- PROD-04: DELETE /products/{id} ----


def test_delete_product_happy_path(app, db_session):
    product = _make_product(db_session)
    client = app.test_client()

    response = client.delete(f"/products/{product.product_id}", headers=_admin_headers())

    assert response.status_code == 200
    assert response.get_json()["status"] == "inactive"

    db_session.delete(product)
    db_session.commit()


def test_delete_product_not_found_returns_404(app):
    client = app.test_client()

    response = client.delete(f"/products/{uuid.uuid4()}", headers=_admin_headers())

    assert response.status_code == 404
    assert response.get_json() == {"error": "Product not found"}


def test_delete_product_already_inactive_returns_409(app, db_session):
    product = _make_product(db_session, status=ProductStatusEnum.inactive)
    client = app.test_client()

    response = client.delete(f"/products/{product.product_id}", headers=_admin_headers())

    assert response.status_code == 409
    assert response.get_json() == {"error": "Product is already inactive"}

    db_session.delete(product)
    db_session.commit()


def test_delete_product_regular_user_returns_403(app, db_session):
    product = _make_product(db_session)
    client = app.test_client()

    response = client.delete(f"/products/{product.product_id}", headers=_regular_user_headers())

    assert response.status_code == 403
    assert response.get_json() == {"error": "Insufficient permissions"}

    db_session.delete(product)
    db_session.commit()


def test_delete_product_without_token_returns_401(app, db_session):
    product = _make_product(db_session)
    client = app.test_client()

    response = client.delete(f"/products/{product.product_id}")

    assert response.status_code == 401
    assert response.get_json() == {"error": "Authentication required"}

    db_session.delete(product)
    db_session.commit()
