from fastapi import APIRouter, Header, Depends, HTTPException
from database import get_db
from schemas.user_schemas import UserResponse, UserCreate, UserUpdate
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from services.user_services import (create_user, get_users, get_user_by_id, 
                                    update_user_by_id, get_user_by_email,
                                    get_user_by_mobile, delete_user_by_id)


routers = APIRouter(prefix="/api/users", tags=["Users"])

def get_company_db(company: str = Header(...)):
    return next(get_db(company)), company

@routers.post("/create-user", response_model=UserResponse)
def create_new_user(user: UserCreate, db_and_company: tuple[Session, str] = Depends(get_company_db)):
    db, company = db_and_company
    try:
        result = create_user(db, user, company)
        return UserResponse(
            id=result[0],
            name=result[1],
            email=result[2],
            mobile_number=result[3],
            role=result[4],
            company=result[5]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@routers.get("/all-users", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 10, db_and_company = Depends(get_company_db)):
    db, company = db_and_company
    rows = get_users(db, skip, limit)
    return [dict(r._mapping) for r in rows]

@routers.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db_and_company = Depends(get_company_db)):
    db, company = db_and_company
    row = get_user_by_id(db, user_id)
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(row._mapping)

@routers.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int, 
    updates: UserUpdate, 
    db_and_company: tuple[Session, str] = Depends(get_company_db)
):
    db, company = db_and_company
    try:
        if updates.email:
            existing_email = get_user_by_email(db, updates.email, company)
            if existing_email and existing_email[0] != user_id:
                raise HTTPException(status_code=400, detail="Email already exists")
        
        # Check if mobile number is being updated and if it already exists
        if updates.mobile_number:
            existing_mobile = get_user_by_mobile(db, updates.mobile_number, company)
            if existing_mobile and existing_mobile[0] != user_id:
                raise HTTPException(status_code=400, detail="Mobile number already exists")
        row = update_user_by_id(db, user_id, updates, company)
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

@routers.delete("/{user_id}", status_code=200)
def delete_user(user_id: int, db_and_company: tuple[Session, str] = Depends(get_company_db)):
    db, company = db_and_company
    row = delete_user_by_id(db, user_id, company)
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(
        content={"message": "User deleted successfully"}
    )
