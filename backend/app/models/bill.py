from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DECIMAL,
    TIMESTAMP,
    text
)

from app.models.business import Base
from sqlalchemy import func

class Bill(Base):

    __tablename__ = "bills"

    bill_id = Column(
        Integer,
        primary_key=True
    )

    business_id = Column(
        Integer,
        ForeignKey("businesses.business_id")
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id")
    )

    total_amount = Column(
        DECIMAL(10,2)
    )

    tax_amount = Column(
        DECIMAL(10,2)
    )

    bill_date = Column(
        TIMESTAMP,
        server_default=text(
            "CURRENT_TIMESTAMP"
        )
    )