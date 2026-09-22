import uuid

import pytest

from app.models.user import RoleEnum, StatusEnum, User
from app.services import auth_service
from app.utils.errors import ConflictError, ValidationError
from app.utils.password import verify_password


def _unique_email():
    return f"service-{uuid.uuid4().hex}@example.com"


def test_register_creates_user_with_forced_role_and_hashed_password(db_session):
    email = _unique_email()

    user = auth_service.register(email, "Sup3r$ecret")

    assert user.role == RoleEnum.regular_user
    assert user.status == StatusEnum.active
    assert user.password_hash != "Sup3r$ecret"
    assert verify_password("Sup3r$ecret", user.password_hash) is True

    db_session.query(User).filter_by(email=email).delete()
    db_session.commit()


def test_register_rejects_duplicate_email(db_session):
    email = _unique_email()
    auth_service.register(email, "Sup3r$ecret")

    with pytest.raises(ConflictError):
        auth_service.register(email, "An0ther$ecret")

    # El rollback automático del UnitOfWork no debe dejar una segunda fila a medias.
    assert db_session.query(User).filter_by(email=email).count() == 1

    db_session.query(User).filter_by(email=email).delete()
    db_session.commit()


def test_register_does_not_commit_if_email_check_raises(db_session):
    email = _unique_email()
    auth_service.register(email, "Sup3r$ecret")

    with pytest.raises(ConflictError):
        auth_service.register(email, "An0ther$ecret")

    # Una sesión completamente distinta (otra conexión) también ve una sola fila:
    # confirma que el UnitOfWork hizo rollback real a nivel de DB, no solo en memoria.
    from sqlalchemy.orm import sessionmaker

    from app.extensions import engine

    other_session = sessionmaker(bind=engine)()
    try:
        assert other_session.query(User).filter_by(email=email).count() == 1
    finally:
        other_session.close()

    db_session.query(User).filter_by(email=email).delete()
    db_session.commit()


@pytest.mark.parametrize(
    "weak_password",
    [
        "Short1!",  # menos de 10 caracteres
        "nouppercase1!",  # sin mayúscula
        "NoSpecialChar1",  # sin carácter especial
    ],
)
def test_register_rejects_password_not_meeting_requirements(weak_password):
    with pytest.raises(ValidationError):
        auth_service.register(_unique_email(), weak_password)
