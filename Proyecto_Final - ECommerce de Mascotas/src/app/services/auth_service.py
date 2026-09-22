import re

from app.auth.jwt_utils import encode_token
from app.extensions import SessionLocal
from app.models.user import RoleEnum, StatusEnum
from app.repositories.user_repository import UserRepository
from app.utils.errors import ConflictError, UnauthorizedError, ValidationError
from app.utils.password import hash_password, verify_password
from app.utils.unit_of_work import UnitOfWork

PASSWORD_MIN_LENGTH = 10
SPECIAL_CHARACTER_PATTERN = re.compile(r"[^A-Za-z0-9]")


def register(email, password):
    if not _password_meets_requirements(password):
        raise ValidationError("Password does not meet security requirements")

    with UnitOfWork(SessionLocal) as uow:
        user_repo = UserRepository(uow.session)

        if user_repo.get_by_email(email) is not None:
            raise ConflictError("Email already registered")

        user = user_repo.create(
            email=email,
            password_hash=hash_password(password),
            role=RoleEnum.regular_user,
            status=StatusEnum.active,
        )

        uow.commit()
        return user


def login(email, password):
    session = SessionLocal()
    user = UserRepository(session).get_by_email(email)

    if user is None or not verify_password(password, user.password_hash):
        raise UnauthorizedError("Invalid credentials")

    return encode_token(str(user.user_id), user.role.value)


def _password_meets_requirements(password):
    if len(password) < PASSWORD_MIN_LENGTH:
        return False
    if not any(character.isupper() for character in password):
        return False
    if not SPECIAL_CHARACTER_PATTERN.search(password):
        return False
    return True
