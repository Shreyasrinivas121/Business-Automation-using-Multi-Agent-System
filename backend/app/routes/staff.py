from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schema.user_schema import StaffCreate

from app.security import hash_password
from app.agents.monitoring_agent import log_activity

router = APIRouter()


@router.post("/staff")
def create_staff(
    staff: StaffCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(User).filter(
        User.email == staff.email
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Email Already Exists"
        )

    new_staff = User(
        username=staff.username,
        email=staff.email,
        password_hash=hash_password(
            staff.password
        ),
        role="staff",
        business_id=staff.business_id
    )

    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)

    log_activity(
        db,
        new_staff.id,
        f"Created Staff User: {new_staff.username}"
    )

    return {
        "message": "Staff Created"
    }


@router.get("/staff")
def get_staff(
    business_id: int,
    db: Session = Depends(get_db)
):

    return (
        db.query(User)
        .filter(
            User.role == "staff",
            User.business_id == business_id
        )
        .all()
    )


@router.delete("/staff/{staff_id}")
def delete_staff(
    staff_id: int,
    business_id: int,
    db: Session = Depends(get_db)
):

    staff = db.query(User).filter(
        User.id == staff_id,
        User.role == "staff",
        User.business_id == business_id
    ).first()

    if not staff:

        raise HTTPException(
            status_code=404,
            detail="Staff Not Found"
        )

    staff_name = staff.username
    staff_user_id = staff.id

    db.delete(staff)
    db.commit()

    try:

        log_activity(
            db,
            staff_user_id,
            f"Deleted Staff User: {staff_name}"
        )

    except:
        pass

    return {
        "message": "Staff Deleted"
    }