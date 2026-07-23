from pydantic import BaseModel

class BusinessCreate(BaseModel):

    business_name: str

    email: str

    phone: str

    address: str

    admin_username: str

    password: str