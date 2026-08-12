
from pydantic import BaseModel, ConfigDict #BaseModel: To define the schema, ConfigDict: To configure the schema behavior
from decimal import Decimal #Same type used by the model product for 'price', so basically it matches
from datetime import datetime #Same type used by the model product for 'entry_date', so basically it matches

class ProductSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True) #model_config it's a 'special dict' that Pydantic reads to set the class
                                                    #from_attributes allows build the schema from objects instead of expect a dict directly
    
    id: int #Validation for int
    name: str #Validation for str
    price: Decimal #Pydantic knows how to converta String JSON like "19.99" to Decimal
    quantity: int #Validation for int
    entry_date: datetime #Pydantic knows how to convert a string ISO ("2026-08-06T10:00:00") to datetime and viceversa



