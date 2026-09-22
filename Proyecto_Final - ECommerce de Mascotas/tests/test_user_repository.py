import uuid

from app.models.user import RoleEnum, StatusEnum, User
from app.repositories.user_repository import UserRepository


def _unique_email():
    return f"repo-{uuid.uuid4().hex}@example.com"


def test_create_adds_user_to_session_without_committing(db_session):
    email = _unique_email()
    repo = UserRepository(db_session)

    user = repo.create(
        email=email,
        password_hash="hashed",
        role=RoleEnum.regular_user,
        status=StatusEnum.active,
    )

    assert user in db_session.new

    db_session.commit()

    assert isinstance(user.user_id, uuid.UUID)
    assert user.role == RoleEnum.regular_user
    assert user.status == StatusEnum.active

    db_session.query(User).filter_by(email=email).delete()
    db_session.commit()


def test_get_by_email_found_and_not_found(db_session):
    email = _unique_email()
    repo = UserRepository(db_session)
    created = repo.create(
        email=email,
        password_hash="hashed",
        role=RoleEnum.regular_user,
        status=StatusEnum.active,
    )
    db_session.commit()

    found = repo.get_by_email(email)
    assert found is not None
    assert found.user_id == created.user_id

    assert repo.get_by_email(_unique_email()) is None

    db_session.query(User).filter_by(email=email).delete()
    db_session.commit()
