from functools import wraps

import jwt as pyjwt
from flask import g, request

from app.auth.jwt_utils import decode_token
from app.utils.errors import ForbiddenError, UnauthorizedError


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise UnauthorizedError("Authentication required")

        parts = auth_header.split(" ", 1)
        if len(parts) != 2 or parts[0] != "Bearer" or not parts[1].strip():
            raise UnauthorizedError("Invalid token")

        token = parts[1].strip()

        try:
            payload = decode_token(token)
        except pyjwt.ExpiredSignatureError:
            raise UnauthorizedError("Session expired")
        except pyjwt.InvalidTokenError:
            raise UnauthorizedError("Invalid token")

        g.current_user = {"user_id": payload["user_id"], "role": payload["role"]}

        return f(*args, **kwargs)

    return wrapper


def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            current_user = getattr(g, "current_user", None)
            if current_user is None or current_user["role"] != required_role:
                raise ForbiddenError("Insufficient permissions")
            return f(*args, **kwargs)

        return wrapper

    return decorator
