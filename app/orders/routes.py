from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session,joinedload

from app.core.database import get_db
from app.auth.dependency import allow_only_user
from app.orders import models as order_models, schemas as order_schemas

import logging

# Create a logger instance for the current module
logger = logging.getLogger(__name__)

# Create an API Router for Orders and Order History
order_router = APIRouter(prefix="/orders", tags=["Orders and Orders History"])


"""
Get the order history for the authenticated user.

Args:
    db (Session): Database session.
    user (User): Authenticated user with role 'user'.

Returns:
    A list of past orders placed by the user.
"""
@order_router.get("/", response_model=list[order_schemas.OrderHistory])
def get_order_history(db: Session = Depends(get_db), user=Depends(allow_only_user)):
    try:
        if user.role != "user":
            logger.warning(f"Access denied to order history for user {user.id} with role {user.role}")
            raise HTTPException(status_code=403, detail="Access denied")

        orders = db.query(order_models.Orders).filter(order_models.Orders.user_id == user.id).all()
        logger.info(f"Order history retrieved for user {user.id} with {len(orders)} orders")
        return orders
    

    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        logger.error(f"Error retrieving order history for user {user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve order history")


"""
Get the details of a specific order placed by the user.

Args:
    order_id (int): ID of the order to retrieve.
    db (Session): Database session.
    user (User): Authenticated user with role 'user'.

Returns:
    OrderDetail: Detailed information about the order including items.

Raises:
    HTTPException: If the order is not found or internal error occurs.
"""
@order_router.get("/{order_id}", response_model=order_schemas.OrderDetail)
def get_order_detail(order_id: int, db: Session = Depends(get_db), user=Depends(allow_only_user)):
    try:
        order = db.query(order_models.Orders).filter(
            order_models.Orders.id == order_id,
            order_models.Orders.user_id == user.id
        ).first()

        if not order:
            logger.warning(f"Order {order_id} not found for user {user.id}")
            raise HTTPException(status_code=404, detail="Order not found")

        logger.info(f"Order {order_id} details retrieved for user {user.id}")
        return order

    
    except HTTPException as http_exception:
        raise http_exception
    
    except Exception as e:
        logger.error(f"Error retrieving order {order_id} for user {user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve order details")
