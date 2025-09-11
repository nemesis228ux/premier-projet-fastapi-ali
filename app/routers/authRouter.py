from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import verify_password
from app.auth.jwt_handler import create_access_token
from app.core.database import get_db



## Model pydantic pour valider login
class LoginRequest(BaseModel):
  username: str
  password: str


router = APIRouter(prefix="/auth", tags=["login"])

@router.post("/login")
def login(form_data: LoginRequest, db: Session = Depends(get_db)):

  user = db.query(User).filter(User.username == form_data.username).first()

  if not user or not verify_password(form_data.password, user.hashed_password):
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="utilsateur ou mot de passe incorrect"
    )
    
  token = create_access_token(data={"sub": str(user.id)})

  return {"access token": token, "token_type": "bearer"} 