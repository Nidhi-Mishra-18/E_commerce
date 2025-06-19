from fastapi import Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.products import models, schemas

"""
Create a new product and store it in the database.

Args:
    db (Session): Database session.
    product (ProductCreate): Product creation schema with name, price, etc.

Returns:
    Products: The newly created product instance.
"""
def create_product(db: Session,product: schemas.ProductCreate):
    product_in_db = models.Products(**product.dict())
    db.add(product_in_db)
    db.commit()
    db.refresh(product_in_db)
    return product_in_db

"""
Retrieve all the product.

Args:
    db (Session): Database session.

Returns:
    List of all the products
"""
def get_all_products(db: Session):
    all_products =  db.query(models.Products).all()
    return all_products

"""
Retrieve a product by its ID 

Args:
    db (Session): Database session.
    product_id (int): Product ID.

Returns:
    Products | None: Product if found, otherwise None.
"""
def get_product_by_id(db: Session, product_id: int):
    search_product = db.query(models.Products).filter(models.Products.id == product_id).first()
    return  search_product


"""
Update the details of an existing product.

Args:
    db: Database session.
    product_id: ID of the product to update.
    product : Fields to update.

Returns:
    Products | None: The updated product instance, or None if not found.
"""
def update_product_details(db: Session, product_id: int, product: schemas.ProductUpdate):
    product_in_db = db.query(models.Products).filter(models.Products.id == product_id).first()
    if product_in_db:
        for key, value in product.dict().items():
            setattr(product_in_db, key, value)
        db.commit()
        db.refresh(product_in_db)
    return product_in_db


"""
Delete a product from the database.

Args:
    db: Database session.
    product_id (int): ID of the product to delete.

Return:
    Products | None: The deleted product instance, or None if not found.
"""
def delete_product(db: Session, product_id: int):
    product_in_db = db.query(models.Products).filter(models.Products.id == product_id).first()
    if product_in_db:
        db.delete(product_in_db)
        db.commit()
    return product_in_db


"""
Retrieve products with optional filters and pagination.

Args:
    db (Session): Database session.
    category (str, optional): Filter by product category.
    min_price (float, optional): Minimum price filter.
    max_price (float, optional): Maximum price filter.
    sort_by (str, optional): Sort products by 'price_asc' or 'price_desc'.
    page (int, optional): Page number for pagination. Defaults to 1.
    page_size (int, optional): Number of products per page. Defaults to 10.

Returns:
    dict: Dictionary containing total number of matching products and paginated items.
"""
def get_products(db: Session, category: str = None, min_price: float = None, max_price: float = None,
                 sort_by: str = None, page: int = 1, page_size: int = 10):
    query = db.query(models.Products)

    if category:
        query = query.filter(models.Products.category == category)

    if min_price is not None:
        query = query.filter(models.Products.price >= min_price)

    if max_price is not None:
        query = query.filter(models.Products.price <= max_price)

    if sort_by == "price_asc":
        query = query.order_by(models.Products.price.asc())
        
    elif sort_by == "price_desc":
        query = query.order_by(models.Products.price.desc())

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return {"total": total, "items": items}


"""
Search products by keyword in name, description, or category.

Args:
    db (Session): Database session.
    keyword (str): Search keyword.

Returns:
    list[Products]: List of matching products.
"""
def search_products(db: Session, keyword: str):
    return db.query(models.Products).filter(
        or_(
            models.Products.name.ilike(f"%{keyword}%"),
            models.Products.description.ilike(f"%{keyword}%"),
            models.Products.category.ilike(f"%{keyword}%")
        )
    ).all()

