from fastapi import APIRouter, Header, Depends, HTTPException
from database import get_db
from schemas.user_schemas import UserResponse, UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from services.user_services import (create_user, get_users, get_user_by_id, 
                                    update_user_by_id, get_user_by_email,
                                    get_user_by_mobile, delete_user_by_id)
from exceptions.exception_handler import NotFoundException


routers = APIRouter(prefix="/api/users", tags=["Users"])

async def get_company_db(company: str = Header(...)):
    async for db in get_db(company):
        return db, company

@routers.post("/create-user", response_model=UserResponse)
async def create_new_user(
    user: UserCreate,
    db_and_company: tuple[AsyncSession, str] = Depends(get_company_db)):
    db, company = db_and_company
    
    result = await create_user(db, user, company)
    return UserResponse(
        id=result[0],
        name=result[1],
        email=result[2],
        mobile_number=result[3],
        role=result[4],
        company=result[5],
        is_active=result[6]
    )


@routers.get("/all-users", response_model=list[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 10,
    db_and_company: tuple[AsyncSession, str] = Depends(get_company_db)
    ):
    db, company = db_and_company
    rows = await get_users(db, company, skip, limit)
    return [dict(r._mapping) for r in rows]

@routers.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db_and_company: tuple[AsyncSession, str] = Depends(get_company_db)):
    db, company = db_and_company
    row = await get_user_by_id(db, user_id, company)
    return dict(row._mapping)

@routers.put("/update/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, 
    updates: UserUpdate, 
    db_and_company: tuple[AsyncSession, str] = Depends(get_company_db)
):
    db, company = db_and_company
    try:
        row = await update_user_by_id(db, user_id, updates, company)
        if not row:
            raise HTTPException(status_code=404, detail="No fields updated")

        return UserResponse(
            id=row[0],
            name=row[1],
            email=row[2],
            mobile_number=row[3],
            role=row[4],
            company=row[5],
            is_active=row[6]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@routers.delete("/delete/{user_id}", status_code=200)
async def delete_user(user_id: int, db_and_company: tuple[AsyncSession, str] = Depends(get_company_db)):
    db, company = db_and_company
    try:
        await delete_user_by_id(db, user_id, company)
        return JSONResponse(
            content={"message": "User deleted successfully"}
        )
    except NotFoundException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
