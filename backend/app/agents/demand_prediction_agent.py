from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.bill import Bill
from app.models.bill_item import BillItem
from app.models.product import Product


def predict_demand(
    db: Session,
    business_id: int
):

    products = (
        db.query(Product)
        .filter(
            Product.business_id == business_id
        )
        .all()
    )

    total_days = (
        db.query(
            func.datediff(
                func.max(Bill.bill_date),
                func.min(Bill.bill_date)
            )
        )
        .scalar()
    )

    total_days = max(
        int(total_days or 1),
        1
    )

    predictions = []

    for product in products:

        total_sold = (
            db.query(
                func.sum(
                    BillItem.quantity
                )
            )
            .join(
                Bill,
                Bill.bill_id == BillItem.bill_id
            )
            .filter(
                BillItem.product_id == product.product_id,
                Bill.business_id == business_id
            )
            .scalar()
        )

        total_sold = float(
            total_sold or 0
        )

        daily_sales_rate = round(
            total_sold / total_days,
            2
        )

        forecast_7_days = round(
            daily_sales_rate * 7,
            2
        )

        forecast_30_days = round(
            daily_sales_rate * 30,
            2
        )

        safety_stock = round(
            forecast_7_days * 0.30,
            2
        )

        recommended_order = max(
            0,
            int(
                forecast_30_days
                + safety_stock
                - product.quantity
            )
        )

        coverage_days = (
            round(
                product.quantity /
                daily_sales_rate,
                1
            )
            if daily_sales_rate > 0
            else 999
        )

        # ==========================
        # RISK ANALYSIS
        # ==========================

        if coverage_days <= 7:

            risk = "High"

            reason = (
                f"Current stock "
                f"({product.quantity}) "
                f"may not satisfy "
                f"forecast demand of "
                f"{forecast_30_days} units. "
                f"Stock could run out within "
                f"{coverage_days} days."
            )

        elif coverage_days <= 15:

            risk = "Medium"

            reason = (
                f"Inventory is sufficient "
                f"for now, but coverage is "
                f"only {coverage_days} days. "
                f"Monitor stock closely."
            )

        else:

            risk = "Low"

            reason = (
                f"Current stock is healthy "
                f"and can support demand for "
                f"approximately "
                f"{coverage_days} days."
            )

        # ==========================
        # SMART DISCOUNT AGENT
        # ==========================

        discount = 0

        discount_reason = (
            "No Discount Needed"
        )

        if (
            forecast_30_days > 0
            and product.quantity >
            forecast_30_days * 3
        ):

            discount = 10

            discount_reason = (
                "Inventory is significantly "
                "higher than expected demand. "
                "Consider a 10% discount "
                "to improve sales."
            )

        elif (
            forecast_30_days > 0
            and product.quantity >
            forecast_30_days * 2
        ):

            discount = 5

            discount_reason = (
                "Inventory is moderately "
                "higher than expected demand. "
                "Consider a 5% discount."
            )

        # ==========================
        # STATUS
        # ==========================

        status = (
            "Order Required"
            if recommended_order > 0
            else "Stock Sufficient"
        )

        predictions.append(
            {
                "product_id":
                product.product_id,

                "product":
                product.product_name,

                "current_stock":
                product.quantity,

                "daily_sales_rate":
                daily_sales_rate,

                "forecast_7_days":
                forecast_7_days,

                "forecast_30_days":
                forecast_30_days,

                "coverage_days":
                coverage_days,

                "recommended_order":
                recommended_order,

                "risk":
                risk,

                "status":
                status,

                "reason":
                reason,

                "discount":
                discount,

                "discount_reason":
                discount_reason
            }
        )

    predictions.sort(
        key=lambda x:
        x["recommended_order"],
        reverse=True
    )

    return predictions