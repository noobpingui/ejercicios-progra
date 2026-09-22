import uuid

import pytest

from app.auth.jwt_utils import decode_token
from app.models.user import User
from app.services import auth_service
from app.utils.errors import UnauthorizedError


def _unique_email():
    return f"login-{uuid.uuid4().hex}@example.com"


def test_login_happy_path_returns_token_with_user_id_and_role(db_session):
    email = _unique_email()
    user = auth_service.register(email, "Sup3r$ecret")

    token = auth_service.login(email, "Sup3r$ecret")
    decoded = decode_token(token)

    assert decoded["user_id"] == str(user.user_id)
    assert decoded["role"] == "regular_user"

    db_session.query(User).filter_by(email=email).delete()
    db_session.commit()


def test_login_rejects_nonexistent_email():
    with pytest.raises(UnauthorizedError, match="Invalid credentials"):
        auth_service.login(_unique_email(), "Whatever1!")


def test_login_rejects_wrong_password(db_session):
    email = _unique_email()
    auth_service.register(email, "Sup3r$ecret")

    with pytest.raises(UnauthorizedError, match="Invalid credentials"):
        auth_service.login(email, "WrongPassword1!")

    db_session.query(User).filter_by(email=email).delete()
    db_session.commit()


def test_login_via_http_happy_path(app, db_session):
    email = _unique_email()
    auth_service.register(email, "Sup3r$ecret")
    client = app.test_client()

    response = client.post("/auth/login", json={"email": email, "password": "Sup3r$ecret"})

    assert response.status_code == 200
    token = response.get_json()["token"]
    decoded = decode_token(token)
    assert decoded["role"] == "regular_user"

    db_session.query(User).filter_by(email=email).delete()
    db_session.commit()


def test_login_via_http_nonexistent_email_returns_401(app):
    client = app.test_client()

    response = client.post(
        "/auth/login", json={"email": _unique_email(), "password": "Whatever1!"}
    )

    assert response.status_code == 401
    assert response.get_json() == {"error": "Invalid credentials"}


def test_login_via_http_wrong_password_returns_same_message(app, db_session):
    email = _unique_email()
    auth_service.register(email, "Sup3r$ecret")
    client = app.test_client()

    response = client.post("/auth/login", json={"email": email, "password": "WrongPassword1!"})

    assert response.status_code == 401
    assert response.get_json() == {"error": "Invalid credentials"}

    db_session.query(User).filter_by(email=email).delete()
    db_session.commit()


def test_login_via_http_missing_field_returns_400(app):
    client = app.test_client()

    response = client.post("/auth/login", json={"email": _unique_email()})

    assert response.status_code == 400
    assert "password" in response.get_json()["error"]
