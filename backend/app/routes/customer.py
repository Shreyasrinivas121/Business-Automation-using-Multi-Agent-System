from app.models.activity_log import ActivityLog
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.schema.customer_schema import CustomerCreate

router = APIRouter()


@router.post("/customers")
def add_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):

    existing_customer = db.query(Customer).filter(
        Customer.customer_name == customer.customer_name,
        Customer.business_id == customer.business_id
    ).first()

    if existing_customer:

        existing_customer.phone = customer.phone
        existing_customer.email = customer.email
        existing_customer.address = customer.address

        db.commit()

        return {
            "message": "Existing Customer Updated"
        }

    new_customer = Customer(
        business_id=customer.business_id,
        customer_name=customer.customer_name,
        phone=customer.phone,
        email=customer.email,
        address=customer.address
    )

    db.add(new_customer)
    db.commit()


    return {
        "message": "Customer Added Successfully"
    }

@router.get("/customers")
def get_customers(
    business_id: int,
    db: Session = Depends(get_db)
):
    customers = (
        db.query(Customer)
        .filter(
            Customer.business_id == business_id
        )
        .all()
    )

    return customers

@router.put("/customers/{customer_id}")
def update_customer(
    customer_id: int,
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):

    existing_customer = db.query(Customer).filter(
    Customer.customer_id == customer_id,
    Customer.business_id == customer.business_id
).first()

    if not existing_customer:
        raise HTTPException(
            status_code=404,
            detail="Customer Not Found"
        )

    existing_customer.customer_name = customer.customer_name
    existing_customer.phone = customer.phone
    existing_customer.email = customer.email
    existing_customer.address = customer.address

    db.commit()


    return {
        "message": "Customer Updated Successfully"
    }


@router.delete("/customers/{customer_id}")
def delete_customer(
    customer_id: int,
    business_id: int,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
    Customer.customer_id == customer_id,
    Customer.business_id == business_id
).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer Not Found"
        )

    customer_name = customer.customer_name

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer Deleted Successfully"
    }