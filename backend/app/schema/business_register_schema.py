from pydantic import BaseModel


class BusinessRegister(BaseModel):

    business_name: str

    admin_username: str

    email: str

    phone: str

    address: str

    password: str