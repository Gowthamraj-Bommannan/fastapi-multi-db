from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.user_schemas import UserCreate

def create_user(db: Session, user: UserCreate, company: str):
    query = text("""
        INSERT INTO users (name, email, mobile_number, role, company)
        VALUES (:name, :email, :mobile, :role, :company)
        RETURNING id, name, email, mobile_number, role, company
    """)
    result = db.execute(query, {
        "name": user.name,
        "email": user.email,
        "mobile": user.mobile_number,
        "role": user.role,
        "company": company
    })
    db.commit()
    return result.fetchone()
