from fastapi import FastAPI

import logging

# Importing Router from various app modules
from app.auth.routes import auth_router
from app.products.routes import admin_product_router
from app.products.routes import public_product_router
from app.cart.routes import cart_router
from app.checkout.routes import checkout_router
from app.orders.routes import order_router


# Initialize Fast API application
app = FastAPI()

# Include API routers for functionality
app.include_router(auth_router)
app.include_router(admin_product_router)
app.include_router(public_product_router)
app.include_router(cart_router)
app.include_router(checkout_router)
app.include_router(order_router)

# Logging Configurations
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("FastAPI application started successfully")