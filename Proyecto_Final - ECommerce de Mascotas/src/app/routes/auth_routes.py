from flask import Blueprint, jsonify, request
from pydantic import ValidationError as PydanticValidationError

from app.schemas.auth_schemas import LoginRequest, RegisterRequest
from app.services import auth_service
from app.utils.errors import ValidationError

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        body = RegisterRequest(**(request.get_json(silent=True) or {}))
    except PydanticValidationError as exc:
        raise ValidationError(_format_pydantic_error(exc))

    user = auth_service.register(body.email, body.password)

    return jsonify({"user_id": str(user.user_id)}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        body = LoginRequest(**(request.get_json(silent=True) or {}))
    except PydanticValidationError as exc:
        raise ValidationError(_format_pydantic_error(exc))

    token = auth_service.login(body.email, body.password)

    return jsonify({"token": token}), 200


def _format_pydantic_error(exc):
    errors = exc.errors()

    missing_fields = [str(error["loc"][0]) for error in errors if error["type"] == "missing"]
    if missing_fields:
        return f"Missing required field(s): {', '.join(missing_fields)}"

    if any(error["loc"] == ("email",) for error in errors):
        return "Invalid email format"

    return "Invalid request body"
