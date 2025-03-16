from sqlalchemy.orm import Session
from typing import List, Dict, Any
from entities import Account
from routes.oauth2.repository import pwd_context, create_user
from dotenv import load_dotenv
import os

load_dotenv()

def seed_users(db: Session, users_data: List[Dict[str, Any]]) -> List[Account]:
    """
    Seed user accounts into the database.
    
    Args:
        db: Database session
        users_data: List of dictionaries containing user data (cus_name, phone_number, password, role)
        
    Returns:
        List of created user accounts
    """
    created_users = []
    
    for user_data in users_data:
        # Check if user already exists
        existing_user = db.query(Account).filter(
            Account.phone_number == user_data["phone_number"]
        ).first()
        
        if not existing_user:
            # Create new user
            user = create_user(
                db=db,
                cus_name=user_data["cus_name"],
                phone_number=user_data["phone_number"],
                password=user_data.get("password"),
                role=user_data.get("role", "user"),
                address=user_data.get("address", "")  # Add address parameter
            )
            created_users.append(user)
                
    return created_users

def seed_initial_data(db: Session):
    """
    Seeds initial data required for application startup.
    This method can be expanded to seed other types of data.
    """
    # Example admin account
    admin_user = {
        "cus_name": "Admin User",
        "phone_number": os.getenv("ADMIN_PHONE", "admin"),
        "password": os.getenv("ADMIN_PASSWORD", "admin@123"),
        "address": "Admin Address",  # Add address field
        "role": "admin"
    }
    
    # Seed admin user
    admin_users = seed_users(db, [admin_user])
    
    # Return result without regular_users
    return {
        "message": "Database seeded successfully",
        "admin_count": len(admin_users)
    }