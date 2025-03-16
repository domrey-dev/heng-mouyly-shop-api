# from fastapi import Depends, HTTPException, status
# from typing import Optional
# from jose import JWTError, jwt
# from fastapi.security import HTTPBearer
# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from sqlalchemy.orm import Session
# from entities import Account
# from dotenv import load_dotenv
# import os

# load_dotenv()

# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")

# http_bearer = HTTPBearer()
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def create_user(db: Session, cus_name: str, phone_number: str, password: Optional[str] = None):
#     user = Account(
#         cus_name=cus_name, 
#         phone_number=phone_number,)
    
#     if password:
#         user.password = pwd_context.hash(password)
#         user.role = "admin"
    
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user

# def create_token(data: dict, expires_delta: timedelta):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
#     access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return access_token

# def verify_access_token(token: str, credentials_exception):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         if payload.get("type") != "access_token":
#             raise credentials_exception
#         return payload
#     except JWTError:
#         raise credentials_exception
    
# def verify_refresh_token(token: str, credentials_exception):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         if payload.get("type") != "refresh_token":
#             raise credentials_exception
#         return payload
#     except JWTError:
#         raise credentials_exception

# def get_current_user(token: str = Depends(http_bearer)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     payload = verify_access_token(token.credentials, credentials_exception)
#     return payload

from fastapi import Depends, HTTPException, status
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from entities import Account
from dotenv import load_dotenv
import os

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, cus_name: str, phone_number: str, password: Optional[str] = None, role: str = "user", address: str = ""):
    user = Account(
        cus_name=cus_name, 
        phone_number=phone_number,
        address=address,  # Add default empty string for address
        role=role
    )
    
    if password:
        user.password = pwd_context.hash(password)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_phone(db: Session, phone_number: str):
    """
    Get a user by phone number
    
    Args:
        db: Database session
        phone_number: Phone number to search for
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(Account).filter(Account.phone_number == phone_number).first()



def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

# Simple user session handler instead of JWT tokens
# This is a placeholder function to maintain compatibility with existing code
# that expects a Depends(get_current_user) dependency
def get_current_user():
    """
    Simplified mock of get_current_user that always returns an admin user
    This replaces token-based authentication to simplify the application
    
    Returns:
        User info dictionary
    """
    # Return a mock admin user to satisfy dependencies
    return {
        "sub": "admin",
        "id": 1,
        "role": "admin"
    }