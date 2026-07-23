from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.models.customer import Customer
from app.models.bill import Bill


def predict_customer_churn(
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

    today = datetime.now()

    for customer in customers:

        last_purchase = (
            db.query(
                func.max(Bill.bill_date)
            )
            .filter(
                Bill.customer_id ==
                customer.customer_id
            )
            .scalar()
        )

        if not last_purchase:

            risk = "High"
            days = 999

        else:

            days = (
                today -
                last_purchase
            ).days

            if days > 30:

                risk = "High"

            elif days > 15:

                risk = "Medium"

            else:

                risk = "Low"

        if risk == "High":

            recommendation = (
                "Send 10% coupon"
            )

        elif risk == "Medium":

            recommendation = (
                "Send promotional offer"
            )

        else:

            recommendation = (
                "Customer Active"
            )

        result.append(
            {
                "customer_id":
                customer.customer_id,

                "customer":
                customer.customer_name,

                "days_since_last_purchase":
                days,

                "risk":
                risk,

                "recommendation":
                recommendation
            }
        )

    return sorted(
        result,
        key=lambda x:
        x["days_since_last_purchase"],
        reverse=True
    )