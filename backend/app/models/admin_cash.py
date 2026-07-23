from sqlalchemy import (
    Column,
    Integer,
    DECIMAL,
    TIMESTAMP,
    ForeignKey,
    text
)

from app.models.business import Base


class AdminCash(Base):

    __tablename__ = "admin_cash"

    cash_id = Column(
        Integer,
        primary_key=True
    )

    business_id = Column(
        Integer,
        ForeignKey(
            "businesses.business_id"
        )
    )

    current_balance = Column(
        DECIMAL(12, 2)
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=text(
            "CURRENT_TIMESTAMP"
        )
    )