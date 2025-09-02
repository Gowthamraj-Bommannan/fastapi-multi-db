from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from exceptions.exception_handler import AlreadyExistsException

async def validate_unique_email(db: AsyncSession,
                          email: str,
                          company: str,
                          exclude_user_id: int | None = None):
    query = text("""
                 SELECT * FROM users WHERE email = :email AND 
                 company = :company AND is_active = TRUE
                 """
                 )
    result = await db.execute(query, {"email": email, "company": company})
    user = result.fetchone()
    if user and (exclude_user_id is None or user[0] != exclude_user_id):
        raise AlreadyExistsException(f"Email {email} already exists")
    
async def validate_unique_mobile(db: AsyncSession,
                          mobile_number: str,
                          company: str,
                          exclude_user_id: int | None = None):
    query = text("""
                 SELECT * FROM users WHERE mobile_number = :mobile_number AND 
                 company = :company AND is_active = TRUE
                 """
                 )
    result = await db.execute(query, {"mobile_number": mobile_number, "company": company})
    user = result.fetchone()
    if user and (exclude_user_id is None or user[0] != exclude_user_id):
        raise AlreadyExistsException(f"Mobile number {mobile_number} already exists")