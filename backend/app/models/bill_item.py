from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DECIMAL
)

from app.models.business import Base

class BillItem(Base):

    __tablename__ = "bill_items"

    item_id = Column(
        Integer,
        primary_key=True
    )

    bill_id = Column(
        Integer,
        ForeignKey("bills.bill_id")
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id")
    )

    quantity = Column(Integer)

    price = Column(
        DECIMAL(10,2)
    )

    subtotal = Column(
        DECIMAL(10,2)
    )