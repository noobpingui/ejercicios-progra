import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.user import RoleEnum, StatusEnum, User


def _unique_email():
    return f"user-{uuid.uuid4().hex}@example.com"


def test_create_user_generates_uuid_and_defaults(db_session):
    email = _unique_email()
    user = User(email=email, password_hash="hashed")
    db_session.add(user)
    db_session.commit()

    assert isinstance(user.user_id, uuid.UUID)
    assert user.role == RoleEnum.regular_user
    assert user.status == StatusEnum.active

    db_session.delete(user)
    db_session.commit()


def test_email_must_be_unique(db_session):
    email = _unique_email()
    db_session.add(User(email=email, password_hash="hashed"))
    db_session.commit()

    db_session.add(User(email=email, password_hash="other_hash"))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    db_session.query(User).filter_by(email=email).delete()
    db_session.commit()


def test_role_can_be_set_to_admin(db_session):
    email = _unique_email()
    user = User(email=email, password_hash="hashed", role=RoleEnum.admin)
    db_session.add(user)
    db_session.commit()

    assert user.role == RoleEnum.admin

    db_session.delete(user)
    db_session.commit()
