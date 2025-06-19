from typing import List
from pydantic import BaseModel, Field
from datetime import datetime

# Order Item schema
class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase :float

    class Config:
        orm_mode = True

# Order history schema
class OrderHistory(BaseModel):
    id: int
    created_at: datetime
    total_amount: float = Field(..., ge=0, description="Total amount should be non-negative")
    status: str = Field(..., min_length=1, description="Status cannot be empty")

    class Config:
        orm_mode = True

# Order Detail schema       
class OrderDetail(BaseModel):
    id: int  
    total_amount: float = Field(..., ge=0, description="Total amount should be non-negative")
    status: str = Field(..., min_length=1)
    created_at: datetime
    items: List[OrderItem]

    class Config:
        orm_mode = True
