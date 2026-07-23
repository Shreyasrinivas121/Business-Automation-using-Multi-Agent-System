from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.product import Product
from app.models.customer import Customer
from app.models.bill import Bill

router = APIRouter()

@router.get("/sales-report")
def sales_report(
    business_id: int,
    db: Session = Depends(get_db)
):

    total_revenue = (
        db.query(
            func.sum(Bill.total_amount)
        )
        .filter(
            Bill.business_id == business_id
        )
        .scalar()
    )

    total_bills = (
        db.query(Bill)
        .filter(
            Bill.business_id == business_id
        )
        .count()
    )

    total_customers = (
        db.query(Customer)
        .filter(
            Customer.business_id == business_id
        )
        .count()
    )

    total_products = (
        db.query(Product)
        .filter(
            Product.business_id == business_id
        )
        .count()
    )

    return {
        "total_revenue": float(
            total_revenue or 0
        ),
        "total_bills": total_bills,
        "total_customers": total_customers,
        "total_products": total_products
    }