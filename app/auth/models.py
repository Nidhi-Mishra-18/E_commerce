import enum
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
    
# Enum for user role
class Role(str,enum.Enum):
    admin="admin"
    user="user"


# SQLAlchemy model representing the user table
class User(Base):
    __tablename__="users"

    id = Column(Integer,primary_key=True, index=True)
    name = Column(String,nullable=False)
    email = Column(String,unique=True,index=True)
    hashed_password = Column(String,nullable=False)
    role = Column(Enum(Role, name="user_roles"), nullable=False, server_default="user")

    cart_items = relationship("Cart", back_populates="user")
    orders = relationship("Orders", back_populates="user")
    reset_tokens = relationship("PasswordResetTokens", back_populates="user")


# SQLAlchemy model representing the Password Reset Tokens table
class PasswordResetTokens(Base):
    __tablename__="password_reset_token"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    token = Column(String,nullable=False)
    expiration_time = Column(DateTime, nullable=False)
    used = Column(Boolean,nullable=False)

    user = relationship("User", back_populates="reset_tokens")


from app.cart.models import Cart
from app.orders.models import Orders
