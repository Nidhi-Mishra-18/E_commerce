from pydantic import BaseModel, EmailStr, Field
from enum import Enum

# Role enum
class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"


# Sign up schema
class SignUpRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: RoleEnum =Field(default=RoleEnum.user)


# Sign in schema
class SignInRequest(BaseModel):
    email: EmailStr
    password: str


# Forgot password schema
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


# Reset password schema
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)


# Token response
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
