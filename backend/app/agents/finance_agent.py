from app.models.admin_cash import AdminCash
from decimal import Decimal

def add_revenue(
    db,
    business_id,
    amount
):

    cash = db.query(
        AdminCash
    ).filter(
        AdminCash.business_id == business_id
    ).first()

    if cash:

        cash.current_balance += Decimal(str(amount))

        db.commit()


def deduct_expense(
    db,
    business_id,
    amount
):

    cash = db.query(
        AdminCash
    ).filter(
        AdminCash.business_id == business_id
    ).first()

    if cash:

        cash.current_balance -= Decimal(str(amount))

        db.commit()


def get_cash_balance(
    db,
    business_id
):

    cash = db.query(
        AdminCash
    ).filter(
        AdminCash.business_id == business_id
    ).first()

    if cash:

        return float(
            cash.current_balance
        )

    return 0