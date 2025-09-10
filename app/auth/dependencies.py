### dependances pour avoir le current user et verifier si c'est un admin

from fastapi import Depends, HTTPException, status
from app.core.database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User
from app.auth.jwt_handler import decode_access_token



# OAuth2PasswordBearer: fastapi va chercher automatiquement 
# le token dans Authorization
oauth_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
  token: str = Depends(oauth_schema), 
  db: Session = Depends(get_db)) -> User:
  
  """Dependance fastapi pr recuperer l'user 
  courant depuis un JWT
  """

  payload = decode_access_token(token=token)
  if payload is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, 
      detail="Token invalide ou expiré",
      headers={"www-Authenticate": "Bearer"},
      )

  user_id = payload.get("sub") # sub c'est le user_id ad on voulait encoder token
  if user_id is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, 
      detail="Token invalide ou expiré",
      headers={"www-Authenticate": "Bearer"},
    )

  user = db.query(User).filter(User.id == int(user_id)).first()
  if user is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail="Cet utilisateur n'existe pas",
    )

  return user # si tout vas bien



## dependance pr administrateur
def admin(current_user: User = Depends(get_current_user)):
  
  """Decorateur pour verifier si 
    current user est un administrateur
  """

  if current_user.role != "admin":
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Vous n'avez pas l'accès a cette fonctionnalité"
    )

  return current_user