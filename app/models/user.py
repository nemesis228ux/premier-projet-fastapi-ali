from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from enum import Enum


class UserRole(Enum):
  user = "user"
  admin = "admin"


class User(Base):
  
  __tablename__ = "users"
  __table_args__ = {"extend_existing": True}

  id: int = Column(Integer, primary_key=True, index=True, nullable=False)
  username: str = Column(String(50), index=True, nullable=False)
  email: str = Column(String(100), index=True, nullable=False, unique=True)
  hashed_password: str = Column(String(500), index=True, nullable=False)
  created_at: datetime = Column(DateTime, default=datetime.utcnow)
  role: str = Column(SqlEnum(UserRole), default=UserRole.user) 

  articles = relationship("Article", back_populates="user")