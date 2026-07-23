from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.agents.finance_agent import get_cash_balance

router = APIRouter()


@router.get("/cash-balance/{business_id}")
def cash_balance(
    business_id: int,
    db: Session = Depends(get_db)
):

    return {
        "cash_balance": get_cash_balance(
            db,
            business_id
        )
    }