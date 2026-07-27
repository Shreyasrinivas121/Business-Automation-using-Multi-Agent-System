from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.product import Product
from app.models.customer import Customer
from app.models.bill import Bill

from app.agents.demand_prediction_agent import predict_demand
from app.agents.customer_loyalty_agent import get_customer_loyalty
from app.agents.business_insights_agent import generate_insights
from app.agents.customer_churn_agent import predict_customer_churn

router = APIRouter()


class AIRequest(BaseModel):
    question: str
    business_id: int

print("AI routes loaded")
@router.post("/ask-ai")
def ask_ai(
    data: AIRequest,
    db: Session = Depends(get_db)
):
    print("========== AI ROUTE CALLED ==========")
    print(data)

    question = data.question.lower().strip()

    # ==========================================
    # Revenue
    # ==========================================
    if "revenue" in question:

        revenue = (
            db.query(func.sum(Bill.total_amount))
            .filter(Bill.business_id == data.business_id)
            .scalar()
        )

        revenue = revenue or 0

        return {
            "answer": f"Total revenue is ₹{revenue}"
        }

    # ==========================================
    # Customers
    # ==========================================
    elif "customer" in question:

        count = (
            db.query(Customer)
            .filter(Customer.business_id == data.business_id)
            .count()
        )

        return {
            "answer": f"Total customers: {count}"
        }

    # ==========================================
    # Bills
    # ==========================================
    elif "bill" in question:

        count = (
            db.query(Bill)
            .filter(Bill.business_id == data.business_id)
            .count()
        )

        return {
            "answer": f"Total bills generated: {count}"
        }

    # ==========================================
    # Low Stock
    # ==========================================
    elif "low stock" in question:

        products = (
            db.query(Product)
            .filter(
                Product.business_id == data.business_id,
                Product.quantity < Product.reorder_level
            )
            .all()
        )

        if not products:
            return {
                "answer": "No low stock products found."
            }

        names = [p.product_name for p in products]

        return {
            "answer": f"Low stock products: {', '.join(names)}"
        }

    # ==========================================
    # Highest Stock
    # ==========================================
    elif "highest stock" in question:

        product = (
            db.query(Product)
            .filter(Product.business_id == data.business_id)
            .order_by(Product.quantity.desc())
            .first()
        )

        if not product:
            return {
                "answer": "No products found."
            }

        return {
            "answer": f"{product.product_name} has highest stock ({product.quantity})"
        }

    # ==========================================
    # Lowest Stock
    # ==========================================
    elif "lowest stock" in question:

        product = (
            db.query(Product)
            .filter(Product.business_id == data.business_id)
            .order_by(Product.quantity.asc())
            .first()
        )

        if not product:
            return {
                "answer": "No products found."
            }

        return {
            "answer": f"{product.product_name} has lowest stock ({product.quantity})"
        }

    # ==========================================
    # Total Products
    # ==========================================
    elif (
        "total products" in question
        or "how many products" in question
        or question == "products"
    ):

        count = (
            db.query(Product)
            .filter(Product.business_id == data.business_id)
            .count()
        )

        return {
            "answer": f"Total products: {count}"
        }

    # ==========================================
    # Default
    # ==========================================
    return {
        "answer": "Sorry, I cannot answer that question yet."
    }


# =====================================================
# Demand Prediction
# =====================================================

@router.get("/demand-predictions")
def get_predictions(
    business_id: int,
    db: Session = Depends(get_db)
):
    return predict_demand(
        db,
        business_id
    )


# =====================================================
# Customer Loyalty
# =====================================================

@router.get("/customer-loyalty")
def customer_loyalty(
    business_id: int,
    db: Session = Depends(get_db)
):
    return get_customer_loyalty(
        db,
        business_id
    )


# =====================================================
# Business Insights
# =====================================================

@router.get("/business-insights")
def business_insights(
    business_id: int,
    db: Session = Depends(get_db)
):
    return generate_insights(
        db,
        business_id
    )


# =====================================================
# Customer Churn
# =====================================================

@router.get("/customer-churn")
def customer_churn(
    business_id: int,
    db: Session = Depends(get_db)
):
    return predict_customer_churn(
        db,
        business_id
    )