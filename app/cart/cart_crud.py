from sqlalchemy.orm import Session
from app.cart import models, schemas

"""
Function to add item to the user cart

Args:
    db: Database Session
    user_id: ID of the user
    item: Data of item to be added into the cart

Return:
    The created or updated cart item
"""
def add_to_cart(db: Session, user_id: int, item: schemas.CartItemCreate):
    # Check if the item already exists in the cart
    existing_product = db.query(models.Cart).filter_by(user_id=user_id, product_id=item.product_id).first()
    
    if existing_product:
        # If it exists, increase the quantity
        existing_product.quantity += item.quantity
        db.commit()
        db.refresh(existing_product)
        return existing_product
    
    # If it does not exist, create a new cart item
    cart_item = models.Cart(**item.dict(), user_id=user_id)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


"""
Function to get all items of user's cart

Args:
    db: Database Session
    user_id: ID of the user

Return:
    All cart item of specific user 
"""
def get_cart(db: Session, user_id: int):
    # Find list of all item in the cart of specific user 
    cart_items = db.query(models.Cart).filter_by(user_id=user_id).all()
    return cart_items


"""
Function to update quatity of specific item in the cart

Args:
    db: Database Session
    user_id: ID of the user
    product_id: Id of the product
    quantity: New quantity value

Return:
    Update cart items or none otherwise
"""
def update_quantity(db: Session, user_id: int, product_id: int, quantity: int):
    # Check if the item already exists in the cart
    item = db.query(models.Cart).filter_by(user_id=user_id, product_id=product_id).first()
    if item:
        item.quantity = quantity
        db.commit()
        db.refresh(item)
        return item
    return None

"""
Function to remove item from user's cart

Args:
    db: Database Session
    user_id: ID of the user
    product_id: Id of the product
    
Return:
    Boolean value (True:If item deleted successfully otherwise False)
"""
def remove_from_cart(db: Session, user_id: int, product_id: int):
    # Check if the item already exists in the cart
    item = db.query(models.Cart).filter_by(user_id=user_id, product_id=product_id).first()
    if item:
        db.delete(item)
        db.commit()
        return True
    return False
