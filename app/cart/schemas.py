from pydantic import BaseModel

# Cart item base schema
class CartItemBase(BaseModel):
    product_id: int
    quantity: int

# Create cart item Schema
class CartItemCreate(CartItemBase):
    pass

# Cart item update schema
class CartItemUpdate(BaseModel):
    quantity: int

# Cart item response schema
class CartItemResponse(CartItemBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
