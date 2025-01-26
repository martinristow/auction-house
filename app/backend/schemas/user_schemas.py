from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    # is_admin: bool
    created_at: datetime

    class Config:
        from_attributes: True



class UserRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: Optional[bool] = False  # Default e False ako ne e stiklirano

