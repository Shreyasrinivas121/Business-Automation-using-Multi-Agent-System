from pydantic import BaseModel


class StaffCreate(BaseModel):

    username: str

    email: str

    password: str

    business_id: int