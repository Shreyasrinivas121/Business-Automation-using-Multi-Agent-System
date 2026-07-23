from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.wholesaler_order import WholesalerOrder
from app.models.product import Product
from app.models.wholesaler import Wholesaler
from fastapi import HTTPException

router = APIRouter()


@router.get("/wholesaler-orders")
def get_orders(
    business_id: int,
    db: Session = Depends(get_db)
):

    orders = (
        db.query(WholesalerOrder)
        .filter(
            WholesalerOrder.business_id == business_id
        )
        .all()
    )

    result = []

    for order in orders:

        product = db.query(
            Product
        ).filter(
            Product.product_id ==
            order.product_id
        ).first()

        wholesaler = db.query(
            Wholesaler
        ).filter(
            Wholesaler.wholesaler_id ==
            order.wholesaler_id
        ).first()

        result.append(
            {
                "order_id":
                    order.order_id,

                "product_name":
                    product.product_name
                    if product else "Unknown",

                "wholesaler_name":
                    wholesaler.wholesaler_name
                    if wholesaler else "Unknown",

                "quantity":
                    order.quantity,

                "purchase_price":
                    float(order.purchase_price),

                "total_cost":
                    float(order.total_cost),

                "status":
                    order.status,

                "created_at":
                    order.created_at
            }
        )

    return result

@router.post("/reject-order/{order_id}")
def reject_order(
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

    order.status = "Rejected"

    db.commit()

    return {
        "message": "Order Rejected"
    }
    
@router.post("/create-suggested-order")
def create_suggested_order(
    product_id: int,
    wholesaler_id: int,
    quantity: int,
    db: Session = Depends(get_db)
):

    product = db.query(
        Product
    ).filter(
        Product.product_id == product_id
    ).first()

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    wholesaler = db.query(
        Wholesaler
    ).filter(
        Wholesaler.wholesaler_id ==
    wholesaler_id
    ).first()

    if not wholesaler:

        raise HTTPException(
            status_code=404,
            detail="No Supplier Found"
        )

    total_cost = (
        quantity *
        float(
            wholesaler.purchase_price
        )
    )

    order = WholesalerOrder(
        business_id=product.business_id,
        product_id=product.product_id,
        wholesaler_id=wholesaler.wholesaler_id,
        quantity=quantity,
        purchase_price=wholesaler.purchase_price,
        total_cost=total_cost,
        status="Pending"
    )

    db.add(order)

    db.commit()

    return {
        "message":
        "Suggested Procurement Order Created"
    }    
    
@router.get("/product-suppliers/{product_id}")
def get_product_suppliers(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = db.query(
        Product
    ).filter(
        Product.product_id == product_id
    ).first()

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    suppliers = (
        db.query(Wholesaler)
        .filter(
            Wholesaler.product_name ==
            product.product_name
        )
        .all()
    )

    result = []

    for supplier in suppliers:

        result.append(
            {
                "wholesaler_id":
                supplier.wholesaler_id,

                "wholesaler_name":
                supplier.wholesaler_name,

                "purchase_price":
                float(
                    supplier.purchase_price
                ),

                "available_quantity":
                supplier.available_quantity
            }
        )

    return result    

@router.post("/apply-discount")
def apply_discount(
    product_id: int,
    discount: float,
    db: Session = Depends(get_db)
):

    product = (
        db.query(Product)
        .filter(
            Product.product_id == product_id
        )
        .first()
    )

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    old_price = float(
        product.price
    )

    new_price = round(
        old_price *
        (100 - discount) / 100,
        2
    )

    product.price = new_price

    db.commit()

    return {
        "message": "Discount Applied",
        "old_price": old_price,
        "new_price": new_price
    }