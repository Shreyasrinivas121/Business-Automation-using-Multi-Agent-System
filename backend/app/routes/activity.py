from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.activity_log import ActivityLog

router = APIRouter()

@router.post("/activity-log")
def add_log(
    data: dict,
    db: Session = Depends(get_db)
):

    log = ActivityLog(
        user_id=data["user_id"],
        business_id=data["business_id"],
        action=data["action"]
    )

    db.add(log)
    db.commit()

    return {
        "message": "Log Added"
    }


@router.get("/activity-logs")
def get_logs(
    business_id: int,
    db: Session = Depends(get_db)
):

    logs = (
    db.query(ActivityLog)
    .filter(
        ActivityLog.business_id == business_id
    )
    .order_by(
        ActivityLog.log_id.desc()
    )
    .all()
)

    return logs