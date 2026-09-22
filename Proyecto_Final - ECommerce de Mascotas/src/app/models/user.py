import enum
import uuid

from sqlalchemy import Column, Enum, String
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import Base


class RoleEnum(enum.Enum):
    regular_user = "regular_user"
    admin = "admin"


class StatusEnum(enum.Enum):
    active = "active"


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.regular_user)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.active)
