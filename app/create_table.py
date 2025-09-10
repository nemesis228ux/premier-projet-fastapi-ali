from core.database import Base, engine
from models.user import User
from models.article import Article

Base.metadata.create_all(bind=engine)
print("Tables crées avec succès ! ")