from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.security_alert import SecurityAlert

router = APIRouter()

@router.get("/security-alerts")
def get_security_alerts(
    business_id: int,
    db: Session = Depends(get_db)
):

    alerts = (
        db.query(SecurityAlert)
        .filter(
            SecurityAlert.business_id == business_id
        )
        .all()
    )

    return alerts


         