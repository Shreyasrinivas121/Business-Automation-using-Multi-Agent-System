from pydantic import BaseModel

class ProductCreate(BaseModel):

    business_id: int

    product_name: str

    category: str

    quantity: int

    price: float

    reorder_level: int