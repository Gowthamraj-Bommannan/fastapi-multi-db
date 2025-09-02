from pydantic import BaseModel, EmailStr, field_validator
import re

class UserBase(BaseModel):
    name: str
    email: EmailStr
    mobile_number: str
    role: str

    @field_validator('mobile_number')
    def validate_mobile_number(cls, v):
        if not re.match(r'^[6-9]\d{9}$', v):
            raise ValueError('Mobile number must be exactly 10 digits and start with 6 to 9')
        return v

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    mobile_number: str | None = None
    role: str | None = None

    @field_validator('mobile_number')
    def validate_mobile_number(cls, v):
        if v is not None:
            if not re.match(r'^[6-9]\d{9}$', v):
                raise ValueError('Mobile number must be exactly 10 digits and start with 6 to 9')
        return v

class UserResponse(UserBase):
    id: int
    company: str

    class Config:
        from_attributes = True