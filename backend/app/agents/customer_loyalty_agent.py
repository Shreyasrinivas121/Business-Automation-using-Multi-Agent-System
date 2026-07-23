from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.customer import Customer
from app.models.bill import Bill


def get_customer_loyalty(
    db: Session,
    business_id: int
):

    customers = (
        db.query(Customer)
        .filter(
            Customer.business_id == business_id
        )
        .all()
    )

    result = []

    for customer in customers:

        total_spent = (
            db.query(
                func.sum(
                    Bill.total_amount
                )
            )
            .filter(
                Bill.customer_id ==
                customer.customer_id
            )
            .scalar()
        )

        total_spent = float(
            total_spent or 0
        )

        total_orders = (
            db.query(
                func.count(
                    Bill.bill_id
                )
            )
            .filter(
                Bill.customer_id ==
                customer.customer_id
            )
            .scalar()
        )

        avg_order_value = round(
            total_spent /
            max(total_orders, 1),
            2
        )

        # =====================
        # LOYALTY TIERS
        # =====================

        if total_spent >= 25000:

            tier = "Platinum"
            discount = 10

        elif total_spent >= 10000:

            tier = "Gold"
            discount = 5

        elif total_spent >= 5000:

            tier = "Silver"
            discount = 2

        else:

            tier = "Bronze"
            discount = 0

        result.append(
            {
                "customer_id":
                customer.customer_id,

                "customer":
                customer.customer_name,

                "total_spent":
                total_spent,

                "orders":
                total_orders,

                "average_order":
                avg_order_value,

                "tier":
                tier,

                "discount":
                discount
            }
        )

    result.sort(
        key=lambda x:
        x["total_spent"],
        reverse=True
    )

    return result

def get_customer_discount(
    total_spent: float
):

    if total_spent >= 25000:
        return 10

    elif total_spent >= 10000:
        return 5

    elif total_spent >= 5000:
        return 2

    return 0
