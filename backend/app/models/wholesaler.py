from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL
)

from app.models.business import Base


class Wholesaler(Base):

    __tablename__ = "wholesalers"

    wholesaler_id = Column(
        Integer,
        primary_key=True
    )

    wholesaler_name = Column(
        String(100)
    )

    product_name = Column(
        String(100)
    )

    purchase_price = Column(
        DECIMAL(10, 2)
    )

    available_quantity = Column(
        Integer
    )