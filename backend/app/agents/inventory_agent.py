from app.models.product import Product
from app.models.wholesaler import Wholesaler
from app.models.wholesaler_order import WholesalerOrder


def update_stock(
    db,
    product,
    quantity_sold
):

    product.quantity -= quantity_sold

    db.commit()

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

            return

        wholesaler = db.query(
            Wholesaler
        ).filter(
            Wholesaler.product_name ==
            product.product_name
        ).order_by(
            Wholesaler.purchase_price.asc()
        ).first()

        if not wholesaler:

            return

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
            business_id=product.business_id,
            product_id=
            product.product_id,

            wholesaler_id=
            wholesaler.wholesaler_id,

            quantity=
            order_qty,

            purchase_price=
            wholesaler.purchase_price,

            total_cost=
            total_cost,

            status="Pending"
        )

        db.add(order)

        db.commit()