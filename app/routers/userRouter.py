from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.schemas.userSchema import UserCreate, UserRead, UserUpdate
from app.core.database import get_db
from app.models.user import User
from app.crud.userCrud import (
  create_user, get_user, get_users, 
  get_user_by_email, update_user, delete_user)
from typing import Annotated
from app.auth.dependencies import get_current_user




router = APIRouter(prefix="/users", tags=['users'])

## creer un  user
@router.post("/", response_model=UserRead)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)) -> Any:
  db_user = create_user(db, user)
  return db_user


## avoir un users par email
@router.get("/search", response_model=UserRead)
def read_user_by_email(q: Annotated[EmailStr, Query()], db: Session = Depends(get_db)) -> Any:

  db_user = get_user_by_email(db, q=q)
  if not db_user:
    raise HTTPException(status_code=404, detail="User not found")

  return db_user


## avoir tous les users
@router.get(
  "/", 
    response_model=list[UserRead], 
    summary="Liste tous les users. la routes est proteger donc faut login"
  )
def read_all_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
  return get_users(db, skip=skip, limit=limit)


## avoir un user
@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):

  db_user = get_user(db, user_id)
  if db_user is None:
    raise HTTPException(status_code=404, detail="User not found")

  return db_user



"""update un user a partir de son email"""
@router.put("/search", response_model=UserRead)
def update_user_by_email(user_data: UserUpdate, q: Annotated[EmailStr, Query()], db: Session = Depends(get_db)) -> Any:
  
  new_db_user = update_user(db, q=q, user_update=user_data)

  if not new_db_user:
    raise HTTPException(status_code=404, detail="User not found")

  return new_db_user


"""supprimer un user a partir de son username"""
@router.delete("/search")
def delete_user_by_username(q= Annotated[str, Query()], db: Session = Depends(get_db)):
  
  user = delete_user(db=db, q=q)

  if user:
    return {"message": f"Utilisateur {user.username} supprimer"}

  raise HTTPException(status_code=404, detail="Cet utilisateur n'existe pas")