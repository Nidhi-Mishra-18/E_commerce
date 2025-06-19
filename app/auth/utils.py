from email.message import EmailMessage
import smtplib
from passlib.context import CryptContext

from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings

password = CryptContext(schemes=["bcrypt"], deprecated="auto")


"""
This function will return the hashed password

Args:
    str: Plain text password

Returns:
    The hashed password by using hash() function
"""
def hash_password(pwd: str):
    return password.hash(pwd)


"""
This function will compare the password 

Args:
    plain_password: Plain text 
    hashed_password: Hashed Value

Returns:
    bool value(True or False)
"""
def verify_password(plain_password, hashed_password):
    return password.verify(plain_password, hashed_password)


"""
Creates a short-lived JWT access token for authentication.

Args:
    data (dict): Information to include in the token, such as user ID.
    expires_delta (timedelta, optional): Time duration after which the token will expire.
                                          Default is set in settings.

Returns:
    str: Encoded JWT access token as a string.
"""
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=settings.access_token_expire_minutes)):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


"""
Creates a long-lived JWT refresh token, usually valid for 7 days.

Args:
    data (dict): Information to include in the token, such as user ID.

Returns:
    str: Encoded JWT refresh token as a string.
"""
def create_refresh_token(data: dict):
    expire = datetime.now() + timedelta(days=7)
    data.update({"exp": expire})
    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)


"""
Sends a password reset email to the user with a secure reset link.

Args:
    to_email (str): The recipient's email address.
    token (str): The unique password reset token generated for the user.

Returns:
    None
"""
def send_reset_password_email(to_email: str, token: str):
    msg = EmailMessage()
    msg["Subject"] = "Reset Your Password"
    msg["From"] = settings.smtp_email
    msg["To"] = to_email
    reset_link = f"http://localhost:3000/reset-password?token={token}"
    msg.set_content(f"Hello,\nWe received a request to reset your password.\nClick the link below to reset it:\n{reset_link}\n\nThis link will expire in 30 minutes. If you didn’t request a password reset, you can safely ignore this email.\n\nThanks,\nYour Support Team")

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(settings.smtp_email, settings.smtp_password)
        server.send_message(msg)