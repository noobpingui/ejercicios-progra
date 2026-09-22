import uuid

import jwt as pyjwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import g, jsonify

from app.auth.decorators import role_required, token_required
from app.auth.jwt_utils import encode_token
from app.config import Config


def _bogus_signature_token(role="admin"):
    bogus_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    bogus_pem = bogus_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return pyjwt.encode(
        {"user_id": str(uuid.uuid4()), "role": role},
        bogus_pem,
        algorithm=Config.JWT_ALGORITHM,
    )


def _register_protected_route(app):
    @app.route("/__test_protected")
    @token_required
    def _protected():
        return jsonify({"user_id": g.current_user["user_id"], "role": g.current_user["role"]})

    @app.route("/__test_admin_only")
    @token_required
    @role_required("admin")
    def _admin_only():
        return jsonify({"ok": True})


def test_missing_authorization_header_returns_401_authentication_required(app):
    _register_protected_route(app)
    client = app.test_client()

    response = client.get("/__test_protected")

    assert response.status_code == 401
    assert response.get_json() == {"error": "Authentication required"}


def test_malformed_authorization_header_returns_401_invalid_token(app):
    _register_protected_route(app)
    client = app.test_client()

    response = client.get("/__test_protected", headers={"Authorization": "Token abc"})

    assert response.status_code == 401
    assert response.get_json() == {"error": "Invalid token"}


def test_valid_token_attaches_current_user_and_continues(app):
    _register_protected_route(app)
    client = app.test_client()
    user_id = str(uuid.uuid4())
    token = encode_token(user_id, "admin")

    response = client.get("/__test_protected", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.get_json() == {"user_id": user_id, "role": "admin"}


def test_expired_token_returns_401_session_expired(app, monkeypatch):
    _register_protected_route(app)
    client = app.test_client()

    monkeypatch.setattr(Config, "JWT_EXP_MINUTES", -1)
    token = encode_token(str(uuid.uuid4()), "admin")

    response = client.get("/__test_protected", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.get_json() == {"error": "Session expired"}


def test_invalid_signature_token_returns_401_invalid_token(app):
    _register_protected_route(app)
    client = app.test_client()
    token = _bogus_signature_token()

    response = client.get("/__test_protected", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.get_json() == {"error": "Invalid token"}


def test_role_required_allows_matching_role(app):
    _register_protected_route(app)
    client = app.test_client()
    token = encode_token(str(uuid.uuid4()), "admin")

    response = client.get("/__test_admin_only", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.get_json() == {"ok": True}


def test_role_required_rejects_non_matching_role(app):
    _register_protected_route(app)
    client = app.test_client()
    token = encode_token(str(uuid.uuid4()), "regular_user")

    response = client.get("/__test_admin_only", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 403
    assert response.get_json() == {"error": "Insufficient permissions"}
