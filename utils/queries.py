from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.user_schemas import UserCreate

def create_new_user(db: Session, user: UserCreate):
    query = text(
        """INSERT INTO users (name, email, mobile_number, role)
        VALUES (:name, :email, :mobile_number, :role)
        RETURNING id, name, email, mobile_number, role"""
        )
    
    result = db.execute(query, {
        "name": user.name,
        "email": user.email,
        "mobile_number": user.mobile_number,
        "role": user.role
    })
    db.commit()
    return result.fetchone()
