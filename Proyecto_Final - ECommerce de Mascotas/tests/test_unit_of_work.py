import uuid

import pytest
from sqlalchemy.orm import sessionmaker

from app.extensions import engine
from app.models.user import User
from app.utils.unit_of_work import UnitOfWork


def _session_factory():
    return sessionmaker(bind=engine)()


def test_commit_persists_changes():
    email = f"uow-{uuid.uuid4().hex}@example.com"

    with UnitOfWork(_session_factory) as uow:
        uow.session.add(User(email=email, password_hash="hashed"))
        uow.commit()

    verify_session = _session_factory()
    try:
        assert verify_session.query(User).filter_by(email=email).first() is not None
    finally:
        verify_session.query(User).filter_by(email=email).delete()
        verify_session.commit()
        verify_session.close()


def test_exception_inside_block_rolls_back_without_commit():
    email = f"uow-{uuid.uuid4().hex}@example.com"

    with pytest.raises(RuntimeError):
        with UnitOfWork(_session_factory) as uow:
            uow.session.add(User(email=email, password_hash="hashed"))
            raise RuntimeError("boom")

    verify_session = _session_factory()
    try:
        assert verify_session.query(User).filter_by(email=email).first() is None
    finally:
        verify_session.close()


def test_exit_closes_the_session():
    with UnitOfWork(_session_factory) as uow:
        session = uow.session

    assert session.in_transaction() is False
