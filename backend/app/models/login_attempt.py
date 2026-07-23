from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    text
)

from app.models.business import Base


class LoginAttempt(Base):

    __tablename__ = "login_attempts"

    attempt_id = Column(
        Integer,
        primary_key=True
    )

    email = Column(
        String(255)
    )

    attempt_count = Column(
        Integer,
        default=0
    )

    last_attempt = Column(
        TIMESTAMP,
        server_default=text(
            "CURRENT_TIMESTAMP"
        )
    )