from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from schemas.user_schemas import UserCreate, UserUpdate
from fastapi import HTTPException
from utils.user_validator import validate_unique_email, validate_unique_mobile
from exceptions.exception_handler import AlreadyExistsException, NotFoundException

async def create_user(db: AsyncSession, user: UserCreate, company: str):
    await validate_unique_email(db, user.email, company)
    await validate_unique_mobile(db, user.mobile_number, company)
    
    query = text("""
        INSERT INTO users (name, email, mobile_number, role, company, is_active)
        VALUES (:name, :email, :mobile, :role, :company, TRUE)
        RETURNING id, name, email, mobile_number, role, company, is_active
    """)
    try:
        result = await db.execute(query, {
            "name": user.name,
            "email": user.email,
            "mobile": user.mobile_number,
            "role": user.role,
            "company": company,
            "is_active": True
        })
        await db.commit()
        return result.fetchone()
    except AlreadyExistsException as e:
        raise AlreadyExistsException("Email or mobile number already exists")
    except Exception as e:
        await db.rollback()
        raise Exception(str(e))


async def get_users(db: AsyncSession, company: str, skip: int = 0, limit: int = 10):
    query = text("""
                SELECT id, name, email, mobile_number, role, company
                FROM users WHERE company = :company AND is_active = TRUE ORDER BY id 
                OFFSET :skip LIMIT :limit
                """)
    try:
        result = await db.execute(query, {"company": company, "skip": skip, "limit": limit})
        return result.fetchall()
    except Exception as e:
        raise Exception(str(e))

async def get_user_by_id(db: AsyncSession, user_id: int, company: str):
    query = text("""SELECT id, name, email, mobile_number, role, company, is_active
                     FROM users WHERE id = :id AND is_active = TRUE""")
    try:
        result = await db.execute(query, {"id": user_id, "company": company})
        user = result.fetchone()
        if not user:
            raise NotFoundException(f"User with ID {user_id} not found")
        return user
    except NotFoundException as e:
        raise
    except Exception as e:
        raise Exception(str(e))

async def update_user_by_id(db: AsyncSession, user_id: int, updates: UserUpdate, company: str):
    if updates.email:
        await validate_unique_email(db, updates.email, company, user_id)
    if updates.mobile_number:
        await validate_unique_mobile(db, updates.mobile_number, company, user_id)
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
    try:
        result = await db.execute(query, params)
        await db.commit()
        user = result.fetchone()
        if not user:
            raise NotFoundException(f"User with ID {user_id} not found")
        return user
    except Exception as e:
        await db.rollback()
        raise Exception(str(e))

async def delete_user_by_id(db: AsyncSession, user_id: int, company: str):
    query = text("""
        UPDATE users 
        SET is_active = FALSE 
        WHERE id = :id AND company = :company AND is_active = TRUE
        RETURNING id, name, email, mobile_number, role, company, is_active
    """)
    try:
        result = await db.execute(query, {"id": user_id, "company": company})
        user = result.fetchone()
        if not user:
            raise NotFoundException(f"User with ID {user_id} not found")
        await db.commit()
        return user
    except NotFoundException:
        raise
    except Exception as e:
        await db.rollback()
        raise Exception(str(e))


async def get_user_by_email(db: AsyncSession, email: str, company: str):
    query = text("""
        SELECT id, name, email, mobile_number, role, company, is_active
        FROM users 
        WHERE email = :email AND company = :company AND is_active = TRUE
    """)
    try:
        result = await db.execute(query, {"email": email, "company": company})
        user = result.fetchone()
        if not user:
            raise NotFoundException(f"User with email {email} not found")
        return user
    except NotFoundException:
        raise
    except Exception as e:
        raise Exception(str(e))

async def get_user_by_mobile(db: AsyncSession, mobile_number: str, company: str):
    query = text("""
        SELECT id, name, email, mobile_number, role, company, is_active
        FROM users 
        WHERE mobile_number = :mobile_number AND company = :company AND is_active = TRUE
    """)
    try:
        result = await db.execute(query, {"mobile_number": mobile_number, "company": company})
        user = result.fetchone()
        if not user:
            raise NotFoundException(f"User with mobile number {mobile_number} not found")
        return user
    except NotFoundException:
        raise
    except Exception as e:
        raise Exception(str(e))