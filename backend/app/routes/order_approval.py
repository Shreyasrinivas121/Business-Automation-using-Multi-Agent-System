from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.product import Product
from app.models.wholesaler import Wholesaler
from app.models.wholesaler_order import WholesalerOrder

from app.agents.finance_agent import deduct_expense
from app.agents.monitoring_agent import log_activity

router = APIRouter()


@router.post("/approve-order/{order_id}")
def approve_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(
        WholesalerOrder
    ).filter(
        WholesalerOrder.order_id == order_id
    ).first()

    if not order:

        raise HTTPException(
            status_code=404,
            detail="Order Not Found"
        )

    if order.status == "Approved":

        raise HTTPException(
            status_code=400,
            detail="Order Already Approved"
        )

    product = db.query(
        Product
    ).filter(
        Product.product_id == order.product_id
    ).first()

    wholesaler = db.query(
        Wholesaler
    ).filter(
        Wholesaler.wholesaler_id ==
        order.wholesaler_id
    ).first()

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    product.quantity += order.quantity

    product.price = float(
        order.purchase_price
    ) * 1.30

    deduct_expense(
        db=db,
        business_id=order.business_id,
        amount=float(
            order.total_cost
        )
    )

    order.status = "Approved"

    db.commit()

    log_activity(
        db=db,
    user_id=1,  # Replace with logged-in user's ID later
    business_id=order.business_id,
    action=f"Approved Purchase Order #{order.order_id}"
    )

    return {
        "message":
        "Order Approved Successfully",

        "product":
        product.product_name,

        "new_stock":
        product.quantity,

        "new_price":
        float(product.price)
    }