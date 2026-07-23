from sqlalchemy import (
    Column,
    Integer,
    DECIMAL,
    String,
    TIMESTAMP,
    text
)

from app.models.business import Base


class WholesalerOrder(Base):

    __tablename__ = "wholesaler_orders"

    order_id = Column(
        Integer,
        primary_key=True
    )
    
    business_id = Column(
    Integer
    )
    
    product_id = Column(
        Integer
    )

    wholesaler_id = Column(
        Integer
    )

    quantity = Column(
        Integer
    )

    purchase_price = Column(
        DECIMAL(10, 2)
    )

    total_cost = Column(
        DECIMAL(10, 2)
    )

    status = Column(
        String(50)
    )

    created_at = Column(
        TIMESTAMP,
        server_default=text(
            "CURRENT_TIMESTAMP"
        )
    )