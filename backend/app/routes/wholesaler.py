from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.wholesaler import Wholesaler
from app.schema.wholesaler_schema import WholesalerCreate

router = APIRouter()


@router.post("/wholesalers")
def add_wholesaler(
    data: WholesalerCreate,
    db: Session = Depends(get_db)
):

    wholesaler = Wholesaler(
        wholesaler_name=data.wholesaler_name,
        product_name=data.product_name,
        purchase_price=data.purchase_price,
        available_quantity=data.available_quantity
    )

    db.add(wholesaler)
    db.commit()

    return {
        "message": "Wholesaler Added"
    }


@router.get("/wholesalers")
def get_wholesalers(
    db: Session = Depends(get_db)
):

    return db.query(
        Wholesaler
    ).all()