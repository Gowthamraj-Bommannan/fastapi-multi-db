from pydantic import BaseModel
from pydantic import EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr
    mobile_number: str
    role: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    mobile_number: str | None = None
    role: str | None = None

class UserResponse(UserBase):
    id: int
    company: str

    class Config:
        from_attributes = True