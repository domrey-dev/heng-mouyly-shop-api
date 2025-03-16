
from fastapi import Depends, HTTPException, status, APIRouter
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv()

from database import get_db
from routes.oauth2.model import UserToken
from routes.oauth2.repository import create_user, pwd_context, get_user_by_phone
from entities import Account
from routes.oauth2.seed import seed_initial_data, seed_users  # Import seeding functions

router = APIRouter(
    tags=["Auth"],
)




@router.post("/sign_in")
def sign_in(form_data: UserToken, db: Session = Depends(get_db)):
    """
    Simplified sign-in function that doesn't use tokens
    """
    user = db.query(Account).filter(Account.phone_number == form_data.phone_number).first()
    if user and pwd_context.verify(form_data.password, user.password):
        # Return user information directly without token
        return {
            'code': status.HTTP_200_OK,
            'status': "Success",
            'result': {
                "user_id": user.cus_id,
                "role": user.role,
                "name": user.cus_name
            }
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
    )

@router.post("/seed_database")
def seed_database_endpoint(db: Session = Depends(get_db)):
    """
    Endpoint to seed the database with initial data.
    This endpoint does not require authentication.
    """
    try:
        result = seed_initial_data(db)
        
        return {
            'code': status.HTTP_200_OK,
            'status': "Success",
            'message': "Database seeded successfully",
            'details': {
                'admin_count': result["admin_count"]
                # Removed 'user_count' since it's no longer in the result
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Seeding failed: {str(e)}"
        )