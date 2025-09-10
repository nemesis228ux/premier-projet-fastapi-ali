## fichier contenant des fonctio pr ceer les token d'authet les decoder
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ACCESS_TOKEN_EXPIRES_MINUITES, ALGORITHM


## func pr creer le token
def create_access_token(data: dict, expire_delta: timedelta | None = None) -> str:
  
  """function pour creer un token a partir des infos du user
    ex: {"sub": user_id}"""

  to_encode = data.copy() # reaser une petite copy
  expiration = datetime.utcnow() + (
    expire_delta or timedelta(minuite=ACCESS_TOKEN_EXPIRES_MINUITES)
    )
  
  to_encode.update({"exp": expiration})

  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  return encoded_jwt ## return le token



## funct pr verifier le token
def decode_access_token(token: str) -> dict[str, None]:
  
  """func pr decoder les tokens. il renvoi les infos
    du token sinon None""" 

  try:
    
    payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM]) ## on chech si tt va bien
    return payload
    
  except JWTError:
    return None