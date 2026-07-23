from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db

from app.models.bill import Bill
from app.models.bill_item import BillItem
from app.models.product import Product
from app.models.customer import Customer

from app.schema.bill_schema import BillCreate

from app.agents.inventory_agent import update_stock
from app.agents.sales_agent import calculate_revenue
from app.agents.monitoring_agent import log_activity
from app.agents.supervisor_agent import process_bill
from app.agents.finance_agent import add_revenue
from app.agents.customer_loyalty_agent import get_customer_discount


router = APIRouter()


@router.post("/bills")
def create_bill(
    bill_data: BillCreate,
    db: Session = Depends(get_db)
):

    subtotal = 0
    products_used = []

    customer_total_spent = (
        db.query(func.sum(Bill.total_amount))
        .filter(Bill.customer_id == bill_data.customer_id)
        .scalar()
    )

    customer_total_spent = float(customer_total_spent or 0)

    loyalty_discount_percent = get_customer_discount(
        customer_total_spent
    )

    for item in bill_data.items:

        product = (
    db.query(Product)
    .filter(
        Product.product_id == item.product_id,
        Product.business_id == bill_data.business_id
    )
    .first()
)

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found"
            )

        if product.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.product_name}"
            )

        item_total = float(product.price) * item.quantity

        subtotal += item_total

        products_used.append(
            {
                "product": product,
                "quantity": item.quantity,
                "subtotal": item_total
            }
        )

    discount_amount = (
        subtotal * loyalty_discount_percent
    ) / 100

    discounted_subtotal = (
        subtotal - discount_amount
    )

    tax = discounted_subtotal * 0.18

    grand_total = calculate_revenue(
        discounted_subtotal,
        tax
    )

    bill = Bill(
        business_id=bill_data.business_id,
        customer_id=bill_data.customer_id,
        total_amount=grand_total,
        tax_amount=tax
    )

    db.add(bill)
    db.commit()
    db.refresh(bill)

    add_revenue(
        db=db,
        business_id=bill.business_id,
        amount=grand_total
    )

    for item in products_used:

        bill_item = BillItem(
            bill_id=bill.bill_id,
            product_id=item["product"].product_id,
            quantity=item["quantity"],
            price=item["product"].price,
            subtotal=item["subtotal"]
        )

        db.add(bill_item)

    grand_total = process_bill(
        db=db,
        bill_id=bill.bill_id,
        products_used=products_used,
        subtotal=subtotal,
        tax=tax
    )

    db.commit()

    customer = (
    db.query(Customer)
    .filter(
        Customer.customer_id == bill.customer_id,
        Customer.business_id == bill_data.business_id
    )
    .first()
)

    return {
        "bill_id": bill.bill_id,
        "customer_name": customer.customer_name,
        "subtotal": subtotal,
        "loyalty_discount_percent": loyalty_discount_percent,
        "discount_amount": discount_amount,
        "tax": tax,
        "grand_total": grand_total,
        "items": [
            {
                "product_name": item["product"].product_name,
                "quantity": item["quantity"],
                "price": float(item["product"].price),
                "subtotal": item["subtotal"]
            }
            for item in products_used
        ]
    }