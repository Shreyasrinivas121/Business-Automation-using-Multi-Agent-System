from sqlalchemy import func

from app.models.bill import Bill
from app.models.customer import Customer
from app.models.product import Product


def generate_summary(
    db,
    business_id: int
):

    revenue = (
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
        "total_revenue": float(revenue or 0),
        "total_bills": total_bills,
        "total_customers": total_customers,
        "total_products": total_products
    }