from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    TIMESTAMP,
    text
)

from app.models.business import Base


class ActivityLog(Base):

    __tablename__ = "activity_logs"

    log_id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )
    
    business_id = Column(
        Integer,
        ForeignKey("businesses.business_id")
    )
    
    action = Column(
        Text
    )

    timestamp = Column(
        TIMESTAMP,
        server_default=text(
            "CURRENT_TIMESTAMP"
        )
    )