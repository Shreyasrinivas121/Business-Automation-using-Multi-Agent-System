from app.models.customer import Customer


def get_customer(
    db,
    customer_id
):

    return db.query(Customer).filter(
        Customer.customer_id == customer_id
    ).first()