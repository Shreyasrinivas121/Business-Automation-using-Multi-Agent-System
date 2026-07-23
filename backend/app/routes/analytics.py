from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.bill import Bill

from app.models.bill_item import BillItem
from app.models.product import Product

router = APIRouter()
@router.get("/sales-trend")
def sales_trend(
    business_id: int,
    db: Session = Depends(get_db)
):

    data = (
        db.query(
            func.date(Bill.bill_date).label("date"),
            func.sum(Bill.total_amount).label("revenue")
        )
        .filter(
            Bill.business_id == business_id
        )
        .group_by(
            func.date(Bill.bill_date)
        )
        .all()
    )

    return [
        {
            "date": str(row.date),
            "revenue": float(row.revenue)
        }
        for row in data
    ]
@router.get("/top-products")
def top_products(
    business_id: int,
    db: Session = Depends(get_db)
):

    data = (
        db.query(
            Product.product_name,
            func.sum(
                BillItem.quantity
            ).label("sold")
        )
        .join(
            BillItem,
            Product.product_id ==
            BillItem.product_id
        )
        .join(
            Bill,
            Bill.bill_id ==
            BillItem.bill_id
        )
        .filter(
            Bill.business_id == business_id
        )
        .group_by(
            Product.product_name
        )
        .order_by(
            func.sum(
                BillItem.quantity
            ).desc()
        )
        .all()
    )

    return [
        {
            "product": row.product_name,
            "sold": int(row.sold)
        }
        for row in data
    ]