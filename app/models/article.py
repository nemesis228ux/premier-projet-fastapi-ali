from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Article(Base):
  
  __tablename__ = "articles"
  __table_args__ = {"extend_existing": True}

  id = Column(Integer, primary_key=True, index=True, nullable=False)
  content = Column(String(200), index=True, nullable=False)

  user_id = Column(Integer, ForeignKey("users.id"))

  user = relationship("User", back_populates="articles")