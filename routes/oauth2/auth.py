from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Define a flag to enable/disable authentication (for seeding)
# You can set this as an environment variable
ENABLE_AUTH = os.getenv("ENABLE_AUTH", "true").lower() == "true"
SEED_MODE = os.getenv("SEED_MODE", "false").lower() == "true"

http_bearer = HTTPBearer()

async def verify_authentication(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db)
):
    """
    Middleware to verify authentication tokens
    When SEED_MODE is enabled, authentication is bypassed
    """
    # Skip authentication for seed routes or if auth is disabled
    if SEED_MODE or not ENABLE_AUTH:
        # Return dummy user data for compatibility
        return {
            "sub": "seed_user",
            "id": 0,
            "role": "admin",
            "is_seed_mode": True
        }
    
    # For non-seed mode, use the existing authentication
    from routes.oauth2.repository import get_current_user
    
    # Extract token and validate
    try:
        # Pass just the token credentials to the existing function
        return get_current_user(credentials.credentials)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )