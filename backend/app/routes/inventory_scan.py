from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.product import Product
from app.models.wholesaler import Wholesaler
from app.models.wholesaler_order import WholesalerOrder

router = APIRouter()


@router.post("/scan-inventory")
def scan_inventory(
    db: Session = Depends(get_db)
):

    products = db.query(
        Product
    ).all()

    orders_created = 0

    for product in products:

        if product.quantity <= product.reorder_level:

            existing_order = db.query(
                WholesalerOrder
            ).filter(
                WholesalerOrder.product_id ==
                product.product_id,

                WholesalerOrder.status ==
                "Pending"
            ).first()

            if existing_order:

                continue

            wholesaler = db.query(
                Wholesaler
            ).filter(
                Wholesaler.product_name ==
                product.product_name
            ).order_by(
                Wholesaler.purchase_price.asc()
            ).first()

            if not wholesaler:

                continue

            order_qty = (
                product.reorder_level * 5
            )

            total_cost = (
                order_qty *
                float(
                    wholesaler.purchase_price
                )
            )

            order = WholesalerOrder(
                product_id=product.product_id,
                wholesaler_id=wholesaler.wholesaler_id,
                quantity=order_qty,
                purchase_price=wholesaler.purchase_price,
                total_cost=total_cost,
                status="Pending"
            )

            db.add(order)

            orders_created += 1

    db.commit()

    return {
        "orders_created": orders_created
    }