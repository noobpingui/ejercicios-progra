import uuid
from typing import List

from pydantic import BaseModel, Field


class AddCartItemRequest(BaseModel):
    product_id: uuid.UUID
    quantity: int = Field(gt=0)


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(gt=0)


class BillingAddress(BaseModel):
    street: str
    city: str
    postal_code: str
    country: str


class CheckoutRequest(BaseModel):
    billing_address: BillingAddress
    payment_method: str


class ReturnItemRequest(BaseModel):
    invoice_item_id: uuid.UUID
    quantity: int = Field(gt=0)


class CreateReturnRequest(BaseModel):
    items: List[ReturnItemRequest] = Field(min_length=1)
