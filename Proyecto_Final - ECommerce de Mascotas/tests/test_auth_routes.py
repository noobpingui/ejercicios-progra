import uuid

from app.models.user import RoleEnum, StatusEnum, User
from app.repositories.user_repository import UserRepository
from app.utils.password import hash_password


def _unique_email():
    return f"route-{uuid.uuid4().hex}@example.com"


def test_register_happy_path(app, db_session):
    email = _unique_email()
    client = app.test_client()

    response = client.post(
        "/auth/register",
        json={"email": email, "password": "Sup3r$ecret"},
    )

    assert response.status_code == 201
    body = response.get_json()
    assert "user_id" in body
    uuid.UUID(body["user_id"])  # no lanza si es un UUID válido

    user = UserRepository(db_session).get_by_email(email)
    assert user is not None
    assert user.role == RoleEnum.regular_user
    assert user.status == StatusEnum.active

    db_session.query(User).filter_by(email=email).delete()
    db_session.commit()


def test_register_duplicate_email_returns_409(app, db_session):
    email = _unique_email()
    UserRepository(db_session).create(
        email=email,
        password_hash=hash_password("Sup3r$ecret"),
        role=RoleEnum.regular_user,
        status=StatusEnum.active,
    )
    db_session.commit()
    client = app.test_client()

    response = client.post(
        "/auth/register",
        json={"email": email, "password": "An0ther$ecret"},
    )

    assert response.status_code == 409
    assert response.get_json() == {"error": "Email already registered"}

    db_session.query(User).filter_by(email=email).delete()
    db_session.commit()


def test_register_weak_password_returns_400(app):
    client = app.test_client()

    response = client.post(
        "/auth/register",
        json={"email": _unique_email(), "password": "short"},
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Password does not meet security requirements"}


def test_register_missing_field_returns_400(app):
    client = app.test_client()

    response = client.post("/auth/register", json={"email": _unique_email()})

    assert response.status_code == 400
    assert "password" in response.get_json()["error"]


def test_register_invalid_email_format_returns_400(app):
    client = app.test_client()

    response = client.post(
        "/auth/register",
        json={"email": "not-an-email", "password": "Sup3r$ecret"},
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid email format"}
