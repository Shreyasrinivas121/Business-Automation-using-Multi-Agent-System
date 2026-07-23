from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.security_alert import SecurityAlert

from app.agents.monitoring_agent import log_activity

router = APIRouter()


@router.post("/resolve-alert/{alert_id}")
def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):

    alert = db.query(
        SecurityAlert
    ).filter(
        SecurityAlert.alert_id == alert_id
    ).first()

    if not alert:

        raise HTTPException(
            status_code=404,
            detail="Alert Not Found"
        )

    alert.status = "Resolved"

    db.commit()

    log_activity(
        db,
        1,
        f"Resolved Security Alert #{alert_id}"
    )

    return {
        "message": "Alert Resolved"
    }