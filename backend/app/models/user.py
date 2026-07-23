from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    TIMESTAMP,
    text
)

from app.models.business import Base

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    username = Column(String(100))

    email = Column(String(200))

    password_hash = Column(String(255))

    role = Column(String(50))

    business_id = Column(
        Integer,
        ForeignKey("businesses.business_id")
    )

    created_at = Column(
        TIMESTAMP,
        server_default=text(
            "CURRENT_TIMESTAMP"
        )
    )