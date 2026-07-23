from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product

router = APIRouter()


@router.get("/inventory-value")
def inventory_value(
    business_id: int,
    db: Session = Depends(get_db)
):

    total = 0

    products = (
    db.query(Product)
    .filter(
        Product.business_id == business_id
    )
    .all()
)

    for product in products:

        total += (
            float(product.price)
            * product.quantity
        )

    return {
        "inventory_value": total
    }