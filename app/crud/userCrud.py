from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.userSchema import UserCreate, UserUpdate
from app.utils.security import hash_password




## crud pr avoir ts les users
def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:

  return db.query(User).offset(skip).limit(limit).all()
  

## crud pr avoir un users
def get_user(db: Session, user_id: int) -> User | None:

  return db.query(User).filter(User.id == user_id).first()
  
  
## crud pr creer un user
def create_user(db: Session, user: UserCreate) -> User:
  
  hashed_pass = hash_password(user.password)
  db_user = User(**user.model_dump(exclude={"password"}), hashed_password = hashed_pass)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user


## chercher un user par son email grace a query()
def get_user_by_email(db: Session, q: str) -> User | None:
  db_user = db.query(User).filter(User.email == q).first()
  return db_user
  


## update un user par son email
def update_user(db: Session, q: str, user_update: UserUpdate) -> User | None:

  db_user = get_user_by_email(db, q=q) 

  if not db_user:
    return None

  if user_update.username:
    db_user.username = user_update.username
  
  if user_update.email:
    db_user.email = user_update.email

  if user_update.password:
    db_user.hashed_password = hash_password(user_update.password)

  db.commit()
  db.refresh(db_user)
  return db_user
    
    
## delete un user par son username
def delete_user(db: Session, q: str):
  
  user = db.query(User).filter(User.username == q).first()
  
  if not user:
    return None

  db.delete(user)
  db.commit()
  return user