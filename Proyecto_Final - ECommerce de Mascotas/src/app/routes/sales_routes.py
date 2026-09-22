import uuid

from flask import Blueprint, g, jsonify, request
from pydantic import ValidationError as PydanticValidationError

from app.auth.decorators import role_required, token_required
from app.schemas.sales_schemas import (
    AddCartItemRequest,
    CheckoutRequest,
    CreateReturnRequest,
    UpdateCartItemRequest,
)
from app.services import sales_service
from app.utils.errors import NotFoundError, ValidationError

sales_bp = Blueprint("carts", __name__, url_prefix="/carts")
invoices_bp = Blueprint("invoices", __name__, url_prefix="/invoices")


@sales_bp.route("", methods=["POST"])
@token_required
def create_cart():
    cart = sales_service.create_cart(_current_user_id())
    return jsonify(_serialize_cart(cart)), 201


@sales_bp.route("", methods=["GET"])
@token_required
def list_carts():
    carts = sales_service.list_pending_carts(_current_user_id())
    return jsonify([_serialize_cart(cart) for cart in carts]), 200


@sales_bp.route("/<cart_id>/items", methods=["POST"])
@token_required
def add_item(cart_id):
    cart_uuid = _parse_uuid_or_404(cart_id, "Cart not found")

    try:
        body = AddCartItemRequest(**(request.get_json(silent=True) or {}))
    except PydanticValidationError as exc:
        raise ValidationError(_format_cart_item_pydantic_error(exc))

    item = sales_service.add_item(cart_uuid, _current_user_id(), body.product_id, body.quantity)

    return jsonify(_serialize_item(item)), 201


@sales_bp.route("/<cart_id>/items/<cart_item_id>", methods=["PATCH"])
@token_required
def update_item(cart_id, cart_item_id):
    cart_uuid = _parse_uuid_or_404(cart_id, "Cart not found")
    item_uuid = _parse_uuid_or_404(cart_item_id, "Item not found in cart")

    try:
        body = UpdateCartItemRequest(**(request.get_json(silent=True) or {}))
    except PydanticValidationError as exc:
        raise ValidationError(_format_cart_item_pydantic_error(exc))

    item = sales_service.update_item_quantity(
        cart_uuid, _current_user_id(), item_uuid, body.quantity
    )

    return jsonify(_serialize_item(item)), 200


@sales_bp.route("/<cart_id>/items/<cart_item_id>", methods=["DELETE"])
@token_required
def remove_item(cart_id, cart_item_id):
    cart_uuid = _parse_uuid_or_404(cart_id, "Cart not found")
    item_uuid = _parse_uuid_or_404(cart_item_id, "Item not found in cart")

    sales_service.remove_item(cart_uuid, _current_user_id(), item_uuid)

    return jsonify({}), 200


@sales_bp.route("/<cart_id>/checkout", methods=["POST"])
@token_required
def checkout(cart_id):
    cart_uuid = _parse_uuid_or_404(cart_id, "Cart not found")

    try:
        body = CheckoutRequest(**(request.get_json(silent=True) or {}))
    except PydanticValidationError as exc:
        raise ValidationError(_format_checkout_pydantic_error(exc))

    invoice = sales_service.checkout(
        cart_uuid,
        _current_user_id(),
        billing_street=body.billing_address.street,
        billing_city=body.billing_address.city,
        billing_postal_code=body.billing_address.postal_code,
        billing_country=body.billing_address.country,
        payment_method=body.payment_method,
    )

    return jsonify({"invoice_number": str(invoice.invoice_number)}), 201


@invoices_bp.route("", methods=["GET"])
@token_required
def list_invoices():
    invoices = sales_service.list_invoices(_current_user_id(), g.current_user["role"])
    return jsonify(invoices), 200


@invoices_bp.route("/<invoice_number>", methods=["GET"])
@token_required
def get_invoice(invoice_number):
    invoice_uuid = _parse_uuid_or_404(invoice_number, "Invoice not found")
    invoice = sales_service.get_invoice(invoice_uuid, _current_user_id(), g.current_user["role"])
    return jsonify(invoice), 200


@invoices_bp.route("/<invoice_number>/returns", methods=["POST"])
@token_required
@role_required("admin")
def create_return(invoice_number):
    invoice_uuid = _parse_uuid_or_404(invoice_number, "Invoice not found")

    try:
        body = CreateReturnRequest(**(request.get_json(silent=True) or {}))
    except PydanticValidationError as exc:
        raise ValidationError(_format_return_pydantic_error(exc))

    items = [
        {"invoice_item_id": item.invoice_item_id, "quantity": item.quantity}
        for item in body.items
    ]

    return_ = sales_service.process_return(invoice_uuid, items)

    return jsonify(_serialize_return(return_)), 201


def _current_user_id():
    return uuid.UUID(g.current_user["user_id"])


def _parse_uuid_or_404(raw_value, message):
    try:
        return uuid.UUID(raw_value)
    except ValueError:
        raise NotFoundError(message)


def _serialize_cart(cart):
    return {
        "cart_id": str(cart.cart_id),
        "status": cart.status.value,
        "items": [_serialize_item(item) for item in cart.items],
    }


def _serialize_item(item):
    return {
        "cart_item_id": str(item.cart_item_id),
        "product_id": str(item.product_id),
        "quantity": item.quantity,
    }


def _serialize_return(return_):
    return {
        "return_id": str(return_.return_id),
        "invoice_number": str(return_.invoice_number),
        "returned_at": return_.returned_at.isoformat(),
        "items": [
            {
                "return_item_id": str(item.return_item_id),
                "invoice_item_id": str(item.invoice_item_id),
                "quantity": item.quantity,
            }
            for item in return_.items
        ],
    }


def _format_cart_item_pydantic_error(exc):
    errors = exc.errors()

    missing_fields = [str(error["loc"][0]) for error in errors if error["type"] == "missing"]
    if missing_fields:
        return f"Missing required field(s): {', '.join(missing_fields)}"

    if any(error["loc"] == ("quantity",) for error in errors):
        return "Quantity must be greater than 0"

    if any(error["loc"] == ("product_id",) for error in errors):
        return "Invalid product_id format"

    return "Invalid request body"


def _format_checkout_pydantic_error(exc):
    errors = exc.errors()

    address_missing_fields = [
        str(error["loc"][-1])
        for error in errors
        if error["loc"] and error["loc"][0] == "billing_address"
    ]
    if address_missing_fields:
        return f"Missing billing address field(s): {', '.join(address_missing_fields)}"

    if any(error["loc"] and error["loc"][0] == "payment_method" for error in errors):
        return "Payment method is required"

    return "Invalid request body"


def _format_return_pydantic_error(exc):
    errors = exc.errors()

    missing_fields = [
        str(error["loc"][-1]) for error in errors if error["type"] == "missing"
    ]
    if missing_fields:
        return f"Missing required field(s): {', '.join(missing_fields)}"

    if any(error["loc"] == ("items",) for error in errors):
        return "At least one return item is required"

    if any(error["loc"] and error["loc"][-1] == "quantity" for error in errors):
        return "Return quantity must be greater than 0"

    if any(error["loc"] and error["loc"][-1] == "invoice_item_id" for error in errors):
        return "Invalid invoice_item_id format"

    return "Invalid request body"
