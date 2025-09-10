from sqlalchemy.orm import Session
from app.models.article import Article
from app.schemas.articleSchema import ArticleCreate, ArticleUpdate


## crud pr avoir ts les articles
def get_articles(db: Session, skip: int = 0, limit: int = 100) -> list[Article]:

  return db.query(Article).offset(skip).limit(limit).all()
  

## crud pr avoir un users
def get_article(db: Session, article_id: int) -> Article | None:

  return db.query(Article).filter(Article.id == article_id).first()
  
  
## crud pr creer un user
def create_article(db: Session, article: ArticleCreate) -> Article:
  
  db_article = Article(**article.model_dump())
  db.add(db_article)
  db.commit()
  db.refresh(db_article)
  return db_article


## update un article a partir de son id
def update_article(db: Session, article_id: int, article_data: ArticleUpdate) -> Article | None:
  
  db_article = db.query(Article).filter(Article.id == article_id).first()

  if not db_article:
    return None

  if article_data.content:
    db_article.content = article_data.content

  if article_data.user_id:
    db_article.user_id = article_data.user_id

  db.commit()
  db.refresh(db_article)
  return db_article
  

## supprimer un article by id
def delete_article(db: Session, article_id: int) -> Article | None:
  
  article = db.query(Article).filter(Article.id == article_id).first()

  if not article:
    return None
  
  db.delete(article)
  db.commit()
  return article