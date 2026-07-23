from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DECIMAL,
    TIMESTAMP,
    text
)

from app.models.business import Base

class Product(Base):

    __tablename__ = "products"

    product_id = Column(
        Integer,
        primary_key=True
    )

    business_id = Column(
        Integer,
        ForeignKey("businesses.business_id")
    )

    product_name = Column(String(200))

    category = Column(String(100))

    quantity = Column(Integer)

    price = Column(DECIMAL(10,2))

    reorder_level = Column(Integer)

    created_at = Column(
        TIMESTAMP,
        server_default=text(
            "CURRENT_TIMESTAMP"
        )
    )