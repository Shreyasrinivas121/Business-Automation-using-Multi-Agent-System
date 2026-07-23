from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schema.business_schema import BusinessCreate
from app.models.business import Business
from app.models.user import User
from app.security import hash_password

router = APIRouter()


@router.post("/register-business")
def register_business(
    business: BusinessCreate,
    db: Session = Depends(get_db)
):
    # Create Business
    new_business = Business(
        business_name=business.business_name,
        email=business.email,
        phone=business.phone,
        address=business.address
    )

    db.add(new_business)
    db.commit()
    db.refresh(new_business)

    # Create Admin User
    admin_user = User(
        username=business.admin_username,
        email=business.email,
        password_hash=hash_password(
            business.password
        ),
        role="admin",
        business_id=new_business.business_id
    )

    db.add(admin_user)
    db.commit()

    return {
        "message": "Business and Admin Created Successfully",
        "business_id": new_business.business_id
    }