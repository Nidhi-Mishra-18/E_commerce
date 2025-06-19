from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.auth.dependency import allow_only_admin
from app.core.database import get_db
from app.products import schemas, products_crud as crud

# Create a logger instance for the current module
logger = logging.getLogger(__name__)

# Create a API Roter for Admin Product Management
admin_product_router = APIRouter(prefix="/admin/products", tags=["Admin Products Management"])

"""
Create a new product (Admin only).

Args:
    product (ProductCreate): Product details.
    db (Session): Database session.
    admin (dict): Admin user info from authentication dependency.

Returns:
    ProductResponse: The newly created product.
"""
@admin_product_router.post("/", response_model=schemas.ProductResponse, status_code=201)
def create(product: schemas.ProductCreate, db: Session = Depends(get_db), admin: dict=Depends(allow_only_admin)):
    
    try:
        created = crud.create_product(db, product)
        logger.info(f"Product created: {created.name}")
        return created
    except Exception as e:
        logger.error(f"Create failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create product")


"""
Retrieve all products (Admin only).

Args:
    db (Session): Database session.
    admin: Admin user info.

Returns:
    List[ProductResponse]: List of all products.
"""

@admin_product_router.get("/", response_model=List[schemas.ProductResponse])
def read_products(db: Session = Depends(get_db), admin:dict = Depends(allow_only_admin)):
    try:
        products = crud.get_all_products(db)
        logger.info("All products retrieved by admin")
        return products
    except Exception as e:
        logger.error(f"Fetch failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch products")


"""    
Retrieve product by ID (Admin only).

Args:
    product_id (int): ID of the product.
    db (Session): SQLAlchemy session.
    admin (dict): Admin user info.

Returns:
    ProductResponse: Product details.
"""
@admin_product_router.get("/{product_id}", response_model=schemas.ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db), admin: dict = Depends(allow_only_admin)):
    try:
        product = crud.get_product_by_id(db, product_id)
        if not product:
            logger.warning(f"Product not found with the id:{product_id}")
            raise HTTPException(status_code=404, detail="Product not found")
        logger.info("Product information found \n{product}")
        return product
    
    except HTTPException as http_exception:
        raise http_exception
    
    except Exception as e:
        logger.error(f"Error fetching product: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch product")


"""
Update product details (Admin only).

Args:
    product_id (int): ID of the product to update.
    product (ProductUpdate): Updated product data.
    db (Session): SQLAlchemy session.
    admin (dict): Admin user info.

Returns:
    ProductResponse: Updated product.
"""
@admin_product_router.put("/{product_id}", response_model=schemas.ProductResponse)
def update(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db), admin: dict = Depends(allow_only_admin)):
    
    try:
        updated = crud.update_product_details(db, product_id, product)
        if not updated:
            raise HTTPException(status_code=404, detail="Product not found")
        return updated
    
    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        logger.error(f"Error updating product: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update product")


"""
Delete a product (Admin only).

Args:
    product_id (int): ID of the product to delete.
    db (Session): Database session.
    admin (dict): Admin user info.

Returns:
    dict: Deletion confirmation message.
"""
@admin_product_router.delete("/{product_id}", status_code=200)
def delete(product_id: int, db: Session = Depends(get_db), admin: dict = Depends(allow_only_admin)):
    
    try:
        deleted = crud.delete_product(db, product_id)
        if not deleted:
            logger.warning(f"Product not found at id:{product_id} ")
            raise HTTPException(status_code=404, detail="Product not found")
        logger.info("Product deleted successfully from the db")
        return {"message": "Product Deleted Successfully"}
    
    except HTTPException as http_exception:
        raise http_exception
    
    except Exception as e:
        logger.error(f"Error deleting product: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete product")


# ------------------------------------------------------------------------------------------------------------
# Create a API Router for Product Information 
public_product_router = APIRouter(prefix="/products", tags=["Products"])

"""
List products with optional filters and pagination.

Args:
    db (Session): SQLAlchemy session.
    category (str, optional): Filter by category.
    min_price (float, optional): Minimum price filter.
    max_price (float, optional): Maximum price filter.
    sort_by (str, optional): Sort by price (asc/desc).
    page (int): Page number.
    page_size (int): Number of items per page.

Returns:
    List[ProductResponse]: List of filtered products.
"""
@public_product_router.get("/", response_model=List[schemas.ProductResponse])
def list_products(
    db: Session = Depends(get_db),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    sort_by: Optional[str] = Query(None, regex="^(price_asc|price_desc)?$"),
    page: int = 1,
    page_size: int = 10,
):
    try:
        result = crud.get_products(db, category, min_price, max_price, sort_by, page, page_size)
        if result["items"]:
            logger.info("Product details found")
            return result["items"]
        else:
            logger.warning("No product Found")
            raise HTTPException(status_code=404,detail="Product not found ")

    except HTTPException as http_exception:   
            raise http_exception

    except Exception as e:
        logger.error(f"Error listing products: {str(e)}")
        raise HTTPException(status_code=500, detail="Error listing products")


"""
Search products by keyword.

Args:
    keyword (str): Keyword to search in name/description.
    db (Session):database Session.

Returns:
    List[ProductResponse]: Matching products.
"""
@public_product_router.get("/search", response_model=List[schemas.ProductResponse])
def search_products(keyword: str, db: Session = Depends(get_db)):
    try:
        results = crud.search_products(db, keyword)

        if results:
            logger.info("Product details found.")
            return results
        else:
            logger.warning(f"No product found with keyword {keyword}")
            raise HTTPException(status_code=404, detail="No products found with that keyword.")
    
    except HTTPException as http_exception:   
            raise http_exception

    except Exception as e:
        logger.exception(f"Error searching products: {str(e)}")
        raise HTTPException(status_code=500, detail="Error searching products")


"""
Get product details by ID.

Args:
    product_id (int): Product ID.
    db (Session): SQLAlchemy session.

Returns:
    ProductResponse: Product details.
"""
@public_product_router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_product_detail(product_id: int, db: Session = Depends(get_db)):
    
    try:
        product = crud.get_product_by_id(db, product_id)
        if not product:
            logger.warning("Product not found in the database")
            raise HTTPException(status_code=404, detail="Product not found with this id")
        logger.info(f"Product details found with product ID :{product_id}")
        return product
    
    except HTTPException as http_exception:   
            raise http_exception
    
    except Exception as e:
        logger.error(f"Error getting product details: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting product details")
