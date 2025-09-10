from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from app.schemas.articleSchema import ArticleMinimal
from typing import Optional
from app.models.user import UserRole


class UserBase(BaseModel):
  
  username: str
  email: EmailStr


class UserCreate(UserBase):
  
  password: str
  role: UserRole = UserRole.user


class UserUpdate(BaseModel):
  
  username: Optional[str] = None
  email: Optional[EmailStr] = None
  password: Optional[str] = None
  role: Optional[UserRole] = None
  


class UserRead(BaseModel):
  
  id: int
  username: str
  email: EmailStr
  created_at: datetime
  articles: list[ArticleMinimal] = []

  class Config:
    orm_mode=True


UserRead.model_rebuild()
ArticleMinimal.model_rebuild() ## a cause des import des utres models // ArticleMinimal
