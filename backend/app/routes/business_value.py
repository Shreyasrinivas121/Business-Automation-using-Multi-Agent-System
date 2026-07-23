from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product
from app.models.admin_cash import AdminCash

router = APIRouter()


@router.get("/business-value/{business_id}")
def business_value(
    business_id: int,
    db: Session = Depends(get_db)
):

    cash = db.query(
        AdminCash
    ).filter(
        AdminCash.business_id == business_id
    ).first()

    cash_balance = (
        float(cash.current_balance)
        if cash else 0
    )

    inventory_value = 0

    products = (
    db.query(Product)
    .filter(
        Product.business_id == business_id
    )
    .all()
)

    for product in products:

        inventory_value += (
            float(product.price)
            * product.quantity
        )

    return {
        "cash_balance": cash_balance,
        "inventory_value": inventory_value,
        "business_value":
        cash_balance + inventory_value
    }