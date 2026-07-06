from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

#Enum/statuses definition
class RentalStatus(str, Enum):
    active = 'active'
    completed = 'completed'

#Models definition
class RentalCreate(BaseModel):
    user_id : int = Field(gt=0)
    car_id : int = Field(gt=0)

class RentalResponse(BaseModel):
    id : int = Field(gt=0)
    user_id : int = Field(gt=0)
    car_id : int = Field(gt=0)
    rental_date : datetime | None = None
    status : RentalStatus

class RentalStatusUpdate(BaseModel):
    status: RentalStatus