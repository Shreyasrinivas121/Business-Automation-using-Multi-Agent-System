from app.models.activity_log import ActivityLog
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product
from app.schema.product_schema import ProductCreate

router = APIRouter()


@router.post("/products")
def add_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):

    existing_product = db.query(Product).filter(
        Product.product_name == product.product_name,
        Product.business_id == product.business_id
    ).first()

    if existing_product:

        existing_product.quantity += product.quantity
        existing_product.price = product.price
        existing_product.category = product.category
        existing_product.reorder_level = product.reorder_level

        db.commit()

        return {
            "message": "Existing Product Updated"
        }

    new_product = Product(
        business_id=product.business_id,
        product_name=product.product_name,
        category=product.category,
        quantity=product.quantity,
        price=product.price,
        reorder_level=product.reorder_level
    )

    db.add(new_product)
    db.commit()
 
    return {
        "message": "Product Added Successfully"
    }

@router.get("/products")
def get_products(
    business_id: int,
    db: Session = Depends(get_db)
):

    products = (
        db.query(Product)
        .filter(
            Product.business_id == business_id
        )
        .all()
    )

    return products


@router.put("/products/{product_id}")
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db)
):

    existing_product = db.query(Product).filter(
        Product.product_id == product_id
    ).first()

    if not existing_product:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    existing_product.product_name = product.product_name
    existing_product.category = product.category
    existing_product.quantity = product.quantity
    existing_product.price = product.price
    existing_product.reorder_level = product.reorder_level

    db.commit()
 
    return {
        "message": "Product Updated Successfully"
    }


@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.product_id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    product_name = product.product_name
 
    db.delete(product)
    db.commit()

    return {
        "message": "Product Deleted Successfully"
    }

@router.get("/low-stock")
def low_stock(
    business_id: int,
    db: Session = Depends(get_db)
):

    products = (
        db.query(Product)
        .filter(
            Product.business_id == business_id,
            Product.quantity < Product.reorder_level
        )
        .all()
    )

    return products