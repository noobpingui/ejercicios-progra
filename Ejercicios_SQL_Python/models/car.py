from pydantic import BaseModel, Field
from enum import Enum

#Enum/statuses definition
class CarStatus(str, Enum):
    available = "available"
    rented = "rented"
    disabled = "disabled"

#Models definition
class CarCreate(BaseModel):
    brand: str = Field(min_length=1)
    model: str = Field(min_length=1)
    year: int = Field(ge=2011, le=2026, description="El anno debe estar entre 1900 y 2026")

class CarResponse(BaseModel):
    id: int = Field(gt=0)
    brand: str = Field(min_length=1)
    model: str = Field(min_length=1)
    year: int = Field(ge=2011, le=2026, description="El anno debe estar entre 1900 y 2026")
    status: CarStatus 

class CarStatusUpdate(BaseModel):
    status: CarStatus