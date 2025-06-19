from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from typing import List

from app.core.database import get_db
from app.cart import schemas, cart_crud as crud
from app.auth.dependency import allow_only_user

import logging

# Create a logger instance  for current module 
logger = logging.getLogger(__name__)

# Create a API router for Cart  
cart_router = APIRouter(prefix="/cart", tags=["Cart"])


"""
Function  to add item in the cart

Args:
    item: The product ID and quantity to add
    db: Database session
    user: The currently authenticated user

Returns:
    The added or updated cart item.
"""
@cart_router.post("/", response_model=schemas.CartItemResponse)
def add_item(item: schemas.CartItemCreate, db: Session = Depends(get_db), user=Depends(allow_only_user)):
    try:
        logger.info(f"User {user.id} is adding item {item.product_id} to cart.")
        cart_item = crud.add_to_cart(db, user.id, item)
        logger.info(f"Item {item.product_id} added to cart for user {user.id}.")
        return cart_item
    
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error! While adding item in the cart")
        raise HTTPException(status_code=500, detail="Error adding item to cart")


"""
Function to add an item to the user's cart.

Args:
    item : The product ID and quantity to add.
    db : Database Session
    user : The currently authenticated user

Returns:
    The added or updated cart item.
"""
@cart_router.get("/", response_model=List[schemas.CartItemResponse])
def view_cart(db: Session = Depends(get_db), user=Depends(allow_only_user)):
    try:
        logger.info(f"Retrieving cart items for user {user.id}")
        cart_items = crud.get_cart(db, user.id)
        logger.info(f"{len(cart_items)} items found in cart for user {user.id}")
        return cart_items

    except SQLAlchemyError as e:
        logger.exception(f"Database error while retrieving cart for user {user.id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving cart items")


"""
Function to update the quantity of a specific item in the user's cart.

Args:
    product_id : ID of the product to update.
    update : New quantity for the item.
    db: Database Session 
    user: The authenticated user making the request.

Returns:
    The updated cart item.
"""
@cart_router.put("/{product_id}", response_model=schemas.CartItemResponse)
def update_item_quantity(product_id: int, update: schemas.CartItemUpdate, db: Session = Depends(get_db), user=Depends(allow_only_user)):
    try:
        logger.info(f"User {user.id} attempting to update item {product_id} to quantity {update.quantity}")
        updated = crud.update_quantity(db, user.id, product_id, update.quantity)

        if not updated:
            logger.warning(f"Item not found in cart for user {user.id}")
            raise HTTPException(status_code=404, detail="Item not found in cart")

        logger.info(f"Cart item {product_id} updated to quantity {update.quantity} for user {user.id}")
        return updated
    
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("Database error while updating cart item ")
        raise HTTPException(status_code=500, detail="Error updating cart item")


"""
Function to delete a specific item from the user's cart.

Args:
    product_id : ID of the product to remove from cart.
    db : Database session 
    user : The authenticated user making the request.

Returns:
    A message indicating successful removal.
"""
@cart_router.delete("/{product_id}")
def delete_item(product_id: int, db: Session = Depends(get_db), user=Depends(allow_only_user)):
    try:
        logger.info(f"User {user.id} attempting to remove item {product_id} from cart.")
        success = crud.remove_from_cart(db, user.id, product_id)
        if not success:
            logger.warning("Item not found in the cart of user:{user.id}")
            raise HTTPException(status_code=404, detail="Item not found in cart")
        return {"message": "Item removed from cart"}
    
    except SQLAlchemyError:
        db.rollback()
        logger.error("Error while deleting the item from the cart")
        raise HTTPException(status_code=500, detail="Error removing cart item")
