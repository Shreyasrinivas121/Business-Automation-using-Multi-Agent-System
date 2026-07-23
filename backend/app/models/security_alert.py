from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    Enum,
    ForeignKey,
    text
)

from app.models.business import Base


class SecurityAlert(Base):

    __tablename__ = "security_alerts"

    alert_id = Column(
        Integer,
        primary_key=True
    )
    
    business_id = Column(
    Integer,
    ForeignKey("businesses.business_id")
)
    
    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    alert_type = Column(
        String(100)
    )

    message = Column(
        Text
    )

    severity = Column(
        Enum(
            "Low",
            "Medium",
            "High"
        )
    )

    status = Column(
        String(20),
        default="Active"
    )

    voice_message = Column(
        Text
    )

    created_at = Column(
        TIMESTAMP,
        server_default=text(
            "CURRENT_TIMESTAMP"
        )
    )