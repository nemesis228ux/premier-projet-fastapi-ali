from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = 'mysql+pymysql://root:@localhost/db_test'

## creer notre engine / db
engine = create_engine(DATABASE_URL, echo=True)

##creer une session
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

## base pour declarer nos modeles
Base = declarative_base()

## function pour avoir une session de notre db
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()