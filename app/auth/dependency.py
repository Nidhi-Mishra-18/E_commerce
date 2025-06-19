from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer

from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.auth import models 
from app.core.config import settings

import logging

# Create a logger instance  for current module 
logger = logging.getLogger(__name__)

# Creating HTTPBearer() object
http_scheme = HTTPBearer()

"""
Function which extract the user info

Args:
    token (HTTPAuthorizationCredentials): Token extracted from the Authorization header.
    db (Session): SQLAlchemy database session.

Returns:
    models.User: The user object found using the ID inside the token.

"""
def extract_user(token: HTTPAuthorizationCredentials= Depends(http_scheme),db: Session = Depends(get_db)) -> models.User:
    try:
        payload = jwt.decode(token.credentials, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        
        user_in_db = db.query(models.User).filter(models.User.id == int(user_id)).first()

        if user_in_db is None:
            logger.warning(f"User with ID {user_id} is not found in the database")
            raise HTTPException(status_code=404, detail="User not found")
        return user_in_db
    
    except HTTPException as http_exception:
        raise http_exception

    except JWTError:
        logger.warning("JWT token decoding Failed")
        raise HTTPException(status_code=401, detail="Invalid token")

"""
Args:
    user (models.User): The current authenticated user extracted from the token.

Returns:
    models.User: The same user object if the user is an admin.

"""
def allow_only_admin(user: models.User = Depends(extract_user)):
    if user.role != "admin":
        logger.warning("Access denied! Admin access required")
        raise HTTPException(status_code=403, detail="Admin access required")
    
    logger.info("Access granted")
    return user

"""
Args:
    user (models.User): The current authenticated user extracted from the token.

Returns:
    models.User: The same user object if the user is a normal user.

"""
def allow_only_user(user: models.User = Depends(extract_user)):
    if user.role != "user":
        logger.warning("Access denied! User access required")
        raise HTTPException(status_code=403, detail="User access required")
    
    logger.info("Access granted")
    return user