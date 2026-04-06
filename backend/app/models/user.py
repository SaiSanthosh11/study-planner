from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    branch: Optional[str] = "CSE"
    semester: Optional[int] = 1

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    name: str
    email: str
    branch: str
    semester: int
    streak: int = 0
    created_at: datetime
