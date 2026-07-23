from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.product import Product
from app.models.bill import Bill
from app.models.customer import Customer
from app.models.security_alert import SecurityAlert


def generate_insights(
    db: Session,
    business_id: int
):

    insights = []

    # ==========================
    # REVENUE
    # ==========================

    revenue = (
        db.query(
            func.sum(Bill.total_amount)
        )
        .filter(
            Bill.business_id == business_id
        )
        .scalar()
    )

    revenue = float(revenue or 0)

    if revenue > 10000:

        insights.append(
            {
                "type": "success",
                "message":
                f"Revenue has reached ₹{revenue:,.2f}."
            }
        )

    # ==========================
    # LOW STOCK
    # ==========================

    low_stock_products = (
        db.query(Product)
        .filter(
            Product.business_id == business_id,
            Product.quantity <= Product.reorder_level
        )
        .all()
    )

    if low_stock_products:

        names = ", ".join(
            [
                p.product_name
                for p in low_stock_products
            ]
        )

        insights.append(
            {
                "type": "warning",
                "message":
                f"Low stock detected for: {names}"
            }
        )

    # ==========================
    # OVERSTOCK
    # ==========================

    overstock_products = (
        db.query(Product)
        .filter(
            Product.business_id == business_id,
            Product.quantity > 100
        )
        .all()
    )

    if overstock_products:

        names = ", ".join(
            [
                p.product_name
                for p in overstock_products
            ]
        )

        insights.append(
            {
                "type": "info",
                "message":
                f"Overstock detected for: {names}. Consider promotions."
            }
        )

    # ==========================
    # LOYAL CUSTOMERS
    # ==========================

    customer_count = (
        db.query(Customer)
        .filter(
            Customer.business_id == business_id
        )
        .count()
    )

    insights.append(
        {
            "type": "success",
            "message":
            f"Customer base currently has {customer_count} customers."
        }
    )

    # ==========================
    # SECURITY ALERTS
    # ==========================

    active_alerts = (
        db.query(SecurityAlert)
        .filter(
            SecurityAlert.status == "Active"
        )
        .count()
    )

    if active_alerts > 0:

        insights.append(
            {
                "type": "danger",
                "message":
                f"{active_alerts} active security alerts require attention."
            }
        )

    else:

        insights.append(
            {
                "type": "success",
                "message":
                "No active security alerts."
            }
        )

    return insights