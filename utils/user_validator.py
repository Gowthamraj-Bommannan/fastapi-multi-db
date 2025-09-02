from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException

def validate_unique_email(db: Session,
                          email: str,
                          company: str,
                          exclude_user_id: int | None = None):
    query = text("""
                 SELECT * FROM users WHERE email = :email AND 
                 company = :company AND is_active = TRUE
                 """
                 )
    result = db.execute(query, {"email": email, "company": company}).fetchone()
    if result and (exclude_user_id is None or result[0] != exclude_user_id):
        raise HTTPException(status_code=400, detail="Email already exists")
    
def validate_unique_mobile(db: Session,
                          mobile_number: str,
                          company: str,
                          exclude_user_id: int | None = None):
    query = text("""
                 SELECT * FROM users WHERE mobile_number = :mobile_number AND 
                 company = :company AND is_active = TRUE
                 """
                 )
    result = db.execute(query, {"mobile_number": mobile_number, "company": company}).fetchone()
    if result and (exclude_user_id is None or result[0] != exclude_user_id):
        raise HTTPException(status_code=400, detail="Mobile number already exists")