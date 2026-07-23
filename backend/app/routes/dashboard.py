from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.agents.report_agent import generate_summary

router = APIRouter()

@router.get("/dashboard")
def dashboard(
    business_id: int,
    db: Session = Depends(get_db)
):

    return generate_summary(
        db,
        business_id
    )