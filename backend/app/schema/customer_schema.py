from pydantic import BaseModel

class CustomerCreate(BaseModel):

    business_id: int

    customer_name: str

    phone: str

    email: str

    address: str