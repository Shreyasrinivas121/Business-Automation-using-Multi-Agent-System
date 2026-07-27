from fastapi import FastAPI
from app.routes.business import router as business_router
from app.routes.login import router as login_router
from app.routes.product import router as product_router
from app.routes.customer import router as customer_router
from app.routes.bill import router as bill_router
from app.routes.dashboard import router as dashboard_router
from app.routes.ai import router as ai_router
from app.routes.report import router as report_router
from app.routes.activity import router as activity_router
from app.routes.analytics import router as analytics_router
from app.routes import security
from app.routes import staff
from app.models.admin_cash import AdminCash
from app.routes import finance
from app.routes import inventory_value
from app.routes import business_value
from app.routes import wholesaler
from app.routes import wholesaler_orders
from app.routes import order_approval
from app.routes import security_actions
from app.routes import inventory_scan
from app.routes import profit_analytics
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request

app = FastAPI()

app.include_router(business_router)
app.include_router(login_router)
app.include_router(product_router)
app.include_router(customer_router)
app.include_router(bill_router)
app.include_router(dashboard_router)
app.include_router(ai_router)
app.include_router(report_router)
app.include_router(activity_router)
app.include_router(analytics_router)
app.include_router(security.router)
app.include_router(staff.router)
app.include_router(finance.router)
app.include_router(inventory_value.router)
app.include_router(business_value.router)
app.include_router(wholesaler.router)
app.include_router(wholesaler_orders.router)
app.include_router(order_approval.router)
app.include_router(security_actions.router)
app.include_router(inventory_scan.router)
app.include_router(profit_analytics.router)

@app.get("/")
def home():
    return {
        "message": "Business Automation API Running"
    }
    
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("========== VALIDATION ERROR ==========")
    print(exc.errors())
    print(await request.body())

    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors()
        }
    )    