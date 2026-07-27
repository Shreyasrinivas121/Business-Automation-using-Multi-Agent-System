from app.agents.inventory_agent import update_stock
from app.agents.sales_agent import calculate_revenue
from app.agents.monitoring_agent import log_activity


def process_bill(
    db,
    bill_id,
    business_id,
    products_used,
    subtotal,
    tax
):

    for item in products_used:

        update_stock(
            db,
            item["product"],
            item["quantity"]
        )

    grand_total = calculate_revenue(
        subtotal,
        tax
    )

    log_activity(
        db=db,
        user_id=1,                # Default admin
        business_id=business_id,
        action=f"Generated Bill #{bill_id}"
    )

    return grand_total