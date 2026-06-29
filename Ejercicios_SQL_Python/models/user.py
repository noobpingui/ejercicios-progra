
from pydantic import BaseModel, Field, EmailStr
from datetime import date
from enum import Enum

#Enum/statuses definition
class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"

#Models definition
class UserCreate(BaseModel):
    name: str = Field(min_length=1) 
    email: EmailStr
    username: str = Field(min_length=1)
    password_hash: str = Field(min_length=8)
    birth_date: date


class UserResponse(BaseModel):
    id: int = Field(gt=0) #validacion que int > 0
    name: str = Field(min_length=1)
    email: EmailStr
    username: str = Field(min_length=1)
    birth_date: date
    status: UserStatus
    is_delinquent: bool = False

class UserStatusUpdate(BaseModel):
    status: UserStatus