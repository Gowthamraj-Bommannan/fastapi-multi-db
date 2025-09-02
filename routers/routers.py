from fastapi import APIRouter, Header, Depends, HTTPException
from database import get_db
from schemas.user_schemas import UserResponse, UserCreate
from sqlalchemy.orm import Session
from services.user_services import create_user


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