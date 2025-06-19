from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependency import allow_only_user
from app.core.database import get_db
from app.cart.models import Cart
from app.orders.models import Orders, OrderItem
from app.auth.models import User

from datetime import datetime

import logging

# Create a logger instance  for current module 
logger=logging.getLogger(__name__)

# Create a API router for checkout
checkout_router = APIRouter(prefix="/checkout", tags=["Checkout"])


"""
Function for order payment 

Args:
    db:Databse Session
    current_user: Only authenticated user with role user

Return:
    Successful payment message with order id and amount
"""
@checkout_router.post("/")
def checkout(db: Session = Depends(get_db), current_user: User = Depends(allow_only_user)):
    try:
        # Fetch all cart items
        cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()

        if not cart_items:
            logger.warning("Cart is empty")
            raise HTTPException(status_code=400, detail="Cart is empty")

        # Create an order
        new_order = Orders(
            user_id=current_user.id,
            created_at=datetime.now(),
            total_amount=sum(item.quantity * item.product.price for item in cart_items)
        )
        new_order.status="paid"
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # Add order items
        for item in cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=item.product.price
            )
            db.add(order_item)

        # Clear cart
        db.query(Cart).filter(Cart.user_id == current_user.id).delete()
        
        db.commit()

        logger.info(f"Payment successful and Order {new_order.id} placed by uses {current_user.id}")
        return {
            "message": "Payment successful and order placed.",
            "order_id": new_order.id,
            "total": new_order.total_amount
        }
    
    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        logger.error(f"Checkout failed for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during checkout.")
