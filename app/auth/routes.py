from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException

from app.auth import models, schemas
from sqlalchemy.orm import Session
from app.auth.dependency import allow_only_admin, allow_only_user
from app.auth.utils import create_access_token, create_refresh_token, hash_password, send_reset_password_email, verify_password
from app.core.database import get_db

import logging

# Create a logger instance  for current module 
logger = logging.getLogger(__name__)

# Create a router for Authentication and User management tasks
auth_router= APIRouter(prefix="/auth",tags=["Authentication and User Management"])


"""
Function for New user(Sign Up)

Args:
    user: The data sent by the user for registration (name, email, password, role)
    db: Database session

Return:
    A success message with user details.
"""
@auth_router.post("/signup",status_code=201)
def sign_up(user: schemas.SignUpRequest, db: Session= Depends(get_db)):
    try:
        # Check that user already exist with the same email or not 
        user_in_db=db.query(models.User).filter(models.User.email == user.email).first()
   
        # If user already exist it will raise an error
        if user_in_db:
            logger.warning(f"Registration failed ! User with {user_in_db.email} is already exists ")
            raise HTTPException(status_code=400,detail="Email already exist")
        
        # If user not exist then hash the password and save the info
        else:
            hashed_pwd= hash_password(user.password)
            create_new_user= models.User(
                name=user.name,
                email=user.email,
                hashed_password=hashed_pwd,
                role=user.role
            )
            db.add(create_new_user)
            db.commit()
            db.refresh(create_new_user)

        logger.info("User registered successfully ")
        return{
            "message":"User Registered Successfully",
            "User":{
            "id":create_new_user.id,
            "name":create_new_user.name,
            "email":create_new_user.email,
            "role":create_new_user.role}
        }
    
    except HTTPException as http_exception:
        raise http_exception
    
    except Exception as e:
        logger.error(f"Error in sign_up: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong during registration")


"""
Function for Already Existing user(Sign in/Login)

Args:
    user: Login credentials (email, password)
    db: Database session

Return:
   Access and Refresh token on succesfull login
"""
@auth_router.post("/signin",response_model=schemas.TokenResponse)
def sign_in(request:schemas.SignInRequest,db: Session= Depends(get_db)):
    try:
        # Check the user is exist in the db or not
        user_in_db=db.query(models.User).filter(models.User.email == request.email).first()
        
        # If email doesn't exist or password is incorrect, raise an exception
        if not user_in_db or not verify_password(request.password,user_in_db.hashed_password):
            logger.warning("Invalid credentials")
            raise HTTPException(status_code=401,detail="Invalid credentials")
        
        # If Login Credential correct then generete access and refresh tokens
        access_token = create_access_token(data={"sub": str(user_in_db.id), "role": user_in_db.role})
        refresh_token = create_refresh_token(data={"sub": str(user_in_db.id)})
        
        logger.info(f"User {user_in_db.email} logged in successfully!") 
        return schemas.TokenResponse(access_token=access_token,refresh_token=refresh_token)
    
    except HTTPException as http_exception:
        raise http_exception
    
    except Exception as e:
        logger.error(f"Error in sign_in: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong during login")


"""
Function to handle forgot password request

Args:
    request: User email id
    db: Database session

Return:
    Message of confirmation
"""
@auth_router.post("/forgot-password")
def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    try:
        # Check if user exists with the given email
        user_in_db = db.query(models.User).filter(models.User.email == request.email).first()

        # If user not found raise an exception
        if not user_in_db:
            logger.warning(f"User with {user_in_db.email} email is not found in the database")
            raise HTTPException(status_code=404, detail="User not found")
        
        else:
            from uuid import uuid4
            
            # Generate random token using uuid4
            token = str(uuid4())

            # Set the expiration time to 30 minutes 
            expiration=datetime.utcnow()+timedelta(minutes=30)

            reset_token = models.PasswordResetTokens(
                user_id=user_in_db.id,
                token=token,
                expiration_time=expiration,
                used=False
            )
            db.add(reset_token)
            db.commit()
            send_reset_password_email(user_in_db.email, token)
        
        logger.info("Password reset mail sent")
        return {"message":"Password reset email sent"}    
    
    except HTTPException as http_exception:
        raise http_exception
    
    except Exception as e:
        logger.error(f"Error in forgot password: {e}")
        raise HTTPException(status_code=500, detail="Failed to send password reset mail")


"""
Function to reset user's password using token

Args:
    request: Reset token and new password
    db: Database session

Return:
    Message confirming password has been reset
"""
@auth_router.post("/auth/reset-password")
def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    try:    
        # Check if the token is valid and not used before
        token_entry = db.query(models.PasswordResetTokens).filter(
            models.PasswordResetTokens.token == request.token,
            models.PasswordResetTokens.used == False
        ).first()

        # If token doesn't exist or has expired, raise an exception
        if not token_entry or token_entry.expiration_time < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Invalid or expired token")

        # Get the user object
        user_in_db = db.query(models.User).filter(models.User.id == token_entry.user_id).first()

        #hash the new password
        user_in_db.hashed_password = hash_password(request.new_password)
        token_entry.used = True
        db.commit()
        logger.info(f"Password of {user_in_db.email} mail is reset successfully")
        return {"message": "Password reset successfully."}
    
    except HTTPException as http_exception:
        raise http_exception
    
    except Exception as e:
        logger.error(f"Error in reset password: {e}")
        raise HTTPException(status_code=500, detail="Failed to rest password")


"""
Admin dashboard route

Args:
    login_user: Authenticated user (must be admin)

Return:
    Welcome message for admin
"""
@auth_router.get("/admin")
def admin_dashboard(login_user: models.User = Depends(allow_only_admin)):
    logger.info(f"Welcome {login_user.name}")
    return {"message": f"Welcome Admin {login_user.name}"}


"""
User profile route

Args:
    login_user: Authenticated user (must be a regular user)

Return:
    Welcome message for user
"""
@auth_router.get("/user")
def user_profile(login_user: models.User = Depends(allow_only_user)):
    logger.info(f"Welcome {login_user.name}")
    return {"message": f"Welcome User {login_user.name}"}
