from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class CreateProductRequest(BaseModel):
    name: str = Field(min_length=1)
    description: Optional[str] = None
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0)


class UpdateProductRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
