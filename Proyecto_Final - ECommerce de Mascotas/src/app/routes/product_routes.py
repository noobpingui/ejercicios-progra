import uuid

from flask import Blueprint, g, jsonify, request
from pydantic import ValidationError as PydanticValidationError

from app.auth.decorators import role_required, token_required
from app.schemas.product_schemas import CreateProductRequest, UpdateProductRequest
from app.services import product_service
from app.utils.errors import NotFoundError, ValidationError

product_bp = Blueprint("products", __name__, url_prefix="/products")


@product_bp.route("", methods=["POST"])
@token_required
@role_required("admin")
def create_product():
    try:
        body = CreateProductRequest(**(request.get_json(silent=True) or {}))
    except PydanticValidationError as exc:
        raise ValidationError(_format_product_pydantic_error(exc))

    product = product_service.create_product(
        name=body.name,
        description=body.description,
        price=body.price,
        stock=body.stock,
    )

    return jsonify({"product_id": str(product.product_id)}), 201


@product_bp.route("", methods=["GET"])
@token_required
def list_products():
    return jsonify(product_service.list_active_products()), 200


@product_bp.route("/<product_id>", methods=["GET"])
@token_required
def get_product(product_id):
    product_uuid = _parse_uuid_or_404(product_id)
    return jsonify(product_service.get_product(product_uuid, g.current_user["role"])), 200


@product_bp.route("/<product_id>", methods=["PUT"])
@token_required
@role_required("admin")
def update_product(product_id):
    product_uuid = _parse_uuid_or_404(product_id)

    try:
        body = UpdateProductRequest(**(request.get_json(silent=True) or {}))
    except PydanticValidationError as exc:
        raise ValidationError(_format_product_pydantic_error(exc))

    product = product_service.update_product(
        product_uuid,
        name=body.name,
        description=body.description,
        price=body.price,
        stock=body.stock,
    )

    return jsonify(product_service.serialize_product(product)), 200


@product_bp.route("/<product_id>", methods=["DELETE"])
@token_required
@role_required("admin")
def delete_product(product_id):
    product_uuid = _parse_uuid_or_404(product_id)
    product = product_service.delete_product(product_uuid)
    return jsonify(product_service.serialize_product(product)), 200


def _parse_uuid_or_404(raw_value):
    try:
        return uuid.UUID(raw_value)
    except ValueError:
        raise NotFoundError("Product not found")


def _format_product_pydantic_error(exc):
    errors = exc.errors()

    missing_fields = [str(error["loc"][0]) for error in errors if error["type"] == "missing"]
    if missing_fields:
        return f"Missing required field(s): {', '.join(missing_fields)}"

    if any(error["loc"] == ("price",) for error in errors):
        return "Price must be greater than 0"

    if any(error["loc"] == ("stock",) for error in errors):
        return "Stock cannot be negative"

    return "Invalid request body"
