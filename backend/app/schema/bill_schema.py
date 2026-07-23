from pydantic import BaseModel
from typing import List

class BillItemRequest(BaseModel):
    product_id: int
    quantity: int

class BillCreate(BaseModel):
    business_id: int
    customer_id: int
    items: List[BillItemRequest]