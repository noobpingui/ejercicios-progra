from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.product_schemas import CreateProductRequest, UpdateProductRequest


def test_create_product_request_valid():
    request = CreateProductRequest(name="Collar", price=Decimal("10.50"), stock=5)

    assert request.name == "Collar"
    assert request.price == Decimal("10.50")
    assert request.stock == 5


@pytest.mark.parametrize("missing_field", ["name", "price", "stock"])
def test_create_product_request_missing_required_field(missing_field):
    data = {"name": "Collar", "price": Decimal("10.50"), "stock": 5}
    del data[missing_field]

    with pytest.raises(ValidationError):
        CreateProductRequest(**data)


def test_create_product_request_rejects_non_positive_price():
    with pytest.raises(ValidationError):
        CreateProductRequest(name="Collar", price=Decimal("0"), stock=5)


def test_create_product_request_rejects_negative_stock():
    with pytest.raises(ValidationError):
        CreateProductRequest(name="Collar", price=Decimal("10.50"), stock=-1)


def test_update_product_request_allows_partial_data():
    request = UpdateProductRequest(price=Decimal("15.00"))

    assert request.price == Decimal("15.00")
    assert request.name is None
    assert request.stock is None


def test_update_product_request_rejects_non_positive_price_when_provided():
    with pytest.raises(ValidationError):
        UpdateProductRequest(price=Decimal("0"))


def test_update_product_request_rejects_negative_stock_when_provided():
    with pytest.raises(ValidationError):
        UpdateProductRequest(stock=-1)
