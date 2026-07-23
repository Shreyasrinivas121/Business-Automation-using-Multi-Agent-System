from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

from app.schema.login_schema import LoginRequest

from app.security import verify_password
from app.auth import create_access_token

from app.agents.login_security_agent import (
    record_failed_login,
    reset_login_attempts)
from app.models.business import Business
from app.schema.business_register_schema import BusinessRegister
import bcrypt

router = APIRouter()

@router.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == login_data.email
    ).first()

    if not user:

        record_failed_login(
            db=db,
            email=login_data.email
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )

    if not verify_password(
        login_data.password,
        user.password_hash
    ):

        record_failed_login(
            db=db,
            email=user.email,
            user=user
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    reset_login_attempts(
        db=db,
        email=user.email
    )

    token = create_access_token(
        {
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
            "business_id": user.business_id
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role,
        "business_id": user.business_id,
        "user_id": user.id
    }

@router.post("/register-business")
def register_business(
    data: BusinessRegister,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(
            User.email == data.email
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    business = Business(
        business_name=data.business_name,
        email=data.email,
        phone=data.phone,
        address=data.address
    )

    db.add(business)

    db.commit()

    db.refresh(business)

    password_hash = bcrypt.hashpw(
        data.password.encode(),
        bcrypt.gensalt()
    ).decode()

    user = User(
        username=data.username,
        email=data.email,
        password_hash=password_hash,
        role="admin",
        business_id=business.business_id
    )

    db.add(user)

    db.commit()

    return {
        "message":
        "Business Registered Successfully",

        "business_id":
        business.business_id
    }        
    
from app.models.business import Business
from app.schema.business_register_schema import BusinessRegister

import bcrypt

@router.post("/register-business")
def register_business(
    data: BusinessRegister,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(
            User.email == data.email
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    business = Business(
        business_name=data.business_name,
        email=data.email,
        phone=data.phone,
        address=data.address
    )

    db.add(business)

    db.commit()

    db.refresh(business)

    password_hash = bcrypt.hashpw(
        data.password.encode(),
        bcrypt.gensalt()
    ).decode()

    user = User(
        username=data.admin_username,
        email=data.email,
        password_hash=password_hash,
        role="admin",
        business_id=business.business_id
    )

    db.add(user)

    db.commit()

    return {
        "message":
        "Business Registered Successfully",

        "business_id":
        business.business_id
    }