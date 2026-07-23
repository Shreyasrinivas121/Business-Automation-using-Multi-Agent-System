from pydantic import BaseModel


class WholesalerCreate(BaseModel):

    wholesaler_name: str

    product_name: str

    purchase_price: float

    available_quantity: int