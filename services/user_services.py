from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.user_schemas import UserCreate, UserUpdate
from fastapi import HTTPException
from utils.user_validator import validate_unique_email, validate_unique_mobile

def create_user(db: Session, user: UserCreate, company: str):
    validate_unique_email(db, user.email, company)
    validate_unique_mobile(db, user.mobile_number, company)
    
    query = text("""
        INSERT INTO users (name, email, mobile_number, role, company, is_active)
        VALUES (:name, :email, :mobile, :role, :company, TRUE)
        RETURNING id, name, email, mobile_number, role, company, is_active
    """)
    result = db.execute(query, {
        "name": user.name,
        "email": user.email,
        "mobile": user.mobile_number,
        "role": user.role,
        "company": company,
        "is_active": True
    })
    db.commit()
    return result.fetchone()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    query = text("SELECT * FROM users WHERE is_active = TRUE ORDER BY id OFFSET :skip LIMIT :limit")
    result = db.execute(query, {"skip": skip, "limit": limit})
    return result.fetchall()

def get_user_by_id(db: Session, user_id: int):
    try:
        query = text("SELECT * FROM users WHERE id = :id AND is_active = TRUE")
        result = db.execute(query, {"id": user_id})
        return result.fetchone()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return result.fetchone()

def update_user_by_id(db: Session, user_id: int, updates: UserUpdate, company: str):
    if updates.email:
        validate_unique_email(db, updates.email, company, user_id)
    if updates.mobile_number:
        validate_unique_mobile(db, updates.mobile_number, company, user_id)
    set_parts = []
    params = {"id": user_id, "company": company}
    
    if updates.name is not None:
        set_parts.append("name = :name")
        params["name"] = updates.name
    if updates.email is not None:
        set_parts.append("email = :email")
        params["email"] = updates.email
    if updates.mobile_number is not None:
        set_parts.append("mobile_number = :mobile")
        params["mobile"] = updates.mobile_number
    if updates.role is not None:
        set_parts.append("role = :role")
        params["role"] = updates.role
    
    if not set_parts:
        return None
    
    query = text(f"""
        UPDATE users SET {', '.join(set_parts)}
        WHERE id = :id AND company = :company AND is_active = TRUE
        RETURNING id, name, email, mobile_number, role, company, is_active
    """)
    result = db.execute(query, params)
    db.commit()
    return result.fetchone()

def delete_user_by_id(db:Session, user_id: int, company: str):
    query = text("""
        UPDATE users 
        SET is_active = FALSE 
        WHERE id = :id AND company = :company AND is_active = TRUE
        RETURNING id, name, email, mobile_number, role, company, is_active
    """)
    result = db.execute(query, {"id": user_id, "company": company})
    db.commit()
    return result.fetchone()

def get_user_by_email(db: Session, email: str, company: str):
    query = text("""
        SELECT id, name, email, mobile_number, role, company, is_active
        FROM users 
        WHERE email = :email AND company = :company AND is_active = TRUE
    """)
    result = db.execute(query, {"email": email, "company": company})
    return result.fetchone()

def get_user_by_mobile(db: Session, mobile_number: str, company: str):
    query = text("""
        SELECT id, name, email, mobile_number, role, company, is_active
        FROM users 
        WHERE mobile_number = :mobile_number AND company = :company AND is_active = TRUE
    """)
    result = db.execute(query, {"mobile_number": mobile_number, "company": company})
    return result.fetchone()