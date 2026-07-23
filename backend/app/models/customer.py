from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey
)

from app.models.business import Base

class Customer(Base):

    __tablename__ = "customers"

    customer_id = Column(
        Integer,
        primary_key=True
    )

    business_id = Column(
        Integer,
        ForeignKey("businesses.business_id")
    )

    customer_name = Column(String(200))

    phone = Column(String(20))

    email = Column(String(100))

    address = Column(Text)