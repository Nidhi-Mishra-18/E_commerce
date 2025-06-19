from pydantic import BaseModel, Field

# Product Base Model Schema
class ProductsBaseModel(BaseModel):
    name: str =Field(...,min_length=1,max_length=50)
    description: str =Field(...,min_length=1)
    price: float =Field(...,gt=0,description="Price must be greater than 0")
    stock: int =Field(...)
    category: str =Field(...)
    image_url: str=Field(...)

# Schema for Create Product
class ProductCreate(ProductsBaseModel):
    pass

# Schema for Update Product
class ProductUpdate(ProductsBaseModel):
    pass

# Schema for Product Response
class ProductResponse(ProductsBaseModel):
    id: int

    class Config:
        orm_mode = True
