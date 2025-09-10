from typing import Optional
from pydantic import BaseModel


class ArticleBase(BaseModel):
  
  content: str


class ArticleCreate(ArticleBase):
  
  user_id: int


class ArticleUpdate(BaseModel):
  
  content: Optional[str] = None
  user_id: Optional[int] = None


class ArticleMinimal(BaseModel):

  id: int

  class Config:
    orm_mode=True
    

class ArticleRead(BaseModel):
  
  id: int
  content: str
  user_id: int

  class Config:
    orm_mode=True