from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.bill import Bill
from app.models.wholesaler_order import WholesalerOrder

router = APIRouter(tags=["Profit Analytics"])


@router.get("/profit/daily")
def get_daily_profit(
    business_id: int,
    from_date: str,
    to_date: str,
    db: Session = Depends(get_db)
):
    revenue_data = (
        db.query(
            func.date(Bill.bill_date).label("date"),
            func.sum(Bill.total_amount).label("revenue")
        )
        .filter(
            Bill.business_id == business_id,
            Bill.bill_date >= from_date,
            Bill.bill_date <= to_date
        )
        .group_by(func.date(Bill.bill_date))
        .all()
    )

    expense_data = (
        db.query(
            func.date(WholesalerOrder.created_at).label("date"),
            func.sum(WholesalerOrder.total_cost).label("expense")
        )
        .filter(
            WholesalerOrder.business_id == business_id,
            WholesalerOrder.status == "Approved",
            WholesalerOrder.created_at >= from_date,
            WholesalerOrder.created_at <= to_date
        )
        .group_by(func.date(WholesalerOrder.created_at))
        .all()
    )

    expense_dict = {
        str(row.date): float(row.expense or 0)
        for row in expense_data
    }

    result = []

    for row in revenue_data:
        revenue = float(row.revenue or 0)
        expense = expense_dict.get(str(row.date), 0)

        result.append({
            "date": str(row.date),
            "revenue": revenue,
            "expense": expense,
            "profit": revenue - expense
        })

    return result

@router.get("/profit/weekly")
def get_weekly_profit(
    business_id: int,
    db: Session = Depends(get_db)
):
    revenue_data = (
        db.query(
            func.yearweek(
                Bill.bill_date
            ).label("week"),
            func.min(
                func.date(Bill.bill_date)
            ).label("start_date"),
            func.max(
                func.date(Bill.bill_date)
            ).label("end_date"),
            func.sum(
                Bill.total_amount
            ).label("revenue")
        )
        .filter(
            Bill.business_id == business_id
        )
        .group_by("week")
        .all()
    )

    expense_data = (
        db.query(
            func.yearweek(
                WholesalerOrder.created_at
            ).label("week"),
            func.sum(
                WholesalerOrder.total_cost
            ).label("expense")
        )
        .filter(
            WholesalerOrder.business_id == business_id,
            WholesalerOrder.status == "Approved"
        )
        .group_by("week")
        .all()
    )

    expense_dict = {
        row.week: float(row.expense or 0)
        for row in expense_data
    }

    result = []

    for row in revenue_data:

        revenue = float(row.revenue or 0)

        expense = expense_dict.get(
            row.week,
            0
        )

        week_label = (
            f"{row.start_date.strftime('%d %b')} - "
            f"{row.end_date.strftime('%d %b')}"
        )

        result.append({
            "week": week_label,
            "revenue": revenue,
            "expense": expense,
            "profit": revenue - expense
        })

    return result

@router.get("/profit/monthly")
def get_monthly_profit(
    business_id: int,
    db: Session = Depends(get_db)
):
    revenue_data = (
        db.query(
            func.date_format(
                Bill.bill_date,
                "%Y-%m"
            ).label("month"),
            func.sum(Bill.total_amount).label("revenue")
        )
        .filter(
            Bill.business_id == business_id
        )
        .group_by("month")
        .all()
    )

    expense_data = (
        db.query(
            func.date_format(
                WholesalerOrder.created_at,
                "%Y-%m"
            ).label("month"),
            func.sum(WholesalerOrder.total_cost).label("expense")
        )
        .filter(
            WholesalerOrder.business_id == business_id,
            WholesalerOrder.status == "Approved"
        )
        .group_by("month")
        .all()
    )

    expense_dict = {
        row.month: float(row.expense or 0)
        for row in expense_data
    }

    result = []

    for row in revenue_data:
        revenue = float(row.revenue or 0)
        expense = expense_dict.get(row.month, 0)

        result.append({
            "month": row.month,
            "revenue": revenue,
            "expense": expense,
            "profit": revenue - expense
        })

    return result


@router.get("/profit/yearly")
def get_yearly_profit(
    business_id: int,
    db: Session = Depends(get_db)
):
    revenue_data = (
        db.query(
            func.year(Bill.bill_date).label("year"),
            func.sum(Bill.total_amount).label("revenue")
        )
        .filter(
            Bill.business_id == business_id
        )
        .group_by("year")
        .all()
    )

    expense_data = (
        db.query(
            func.year(WholesalerOrder.created_at).label("year"),
            func.sum(WholesalerOrder.total_cost).label("expense")
        )
        .filter(
            WholesalerOrder.business_id == business_id,
            WholesalerOrder.status == "Approved"
        )
        .group_by("year")
        .all()
    )

    expense_dict = {
        row.year: float(row.expense or 0)
        for row in expense_data
    }

    result = []

    for row in revenue_data:
        revenue = float(row.revenue or 0)
        expense = expense_dict.get(row.year, 0)

        result.append({
            "year": row.year,
            "revenue": revenue,
            "expense": expense,
            "profit": revenue - expense
        })

    return result