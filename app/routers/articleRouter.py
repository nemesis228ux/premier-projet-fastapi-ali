from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from app.schemas.articleSchema import ArticleCreate, ArticleRead, ArticleUpdate
from app.core.database import get_db
from app.models.article import Article
from app.crud.articleCrud import get_article, get_articles, delete_article, create_article, update_article
from app.auth.dependencies import get_current_user



router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/", response_model=list[ArticleRead], summary="Lister tous les aticles")
def read_all_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  return get_articles(db, skip=skip, limit=limit)


"""mettre a jour un article a partir de son id"""
@router.put("/{article_id}", response_model=ArticleRead)
def update_article_by_id(article_data: ArticleUpdate, article_id: Annotated[int, Path()], db: Session = Depends(get_db)) -> Any:
  
  new_article = update_article(db, article_id=article_id, article_data=article_data)

  if not new_article:
    raise HTTPException(status_code=404, detail="Article introuvable")

  return new_article


"""obtenir un article par id"""
@router.get("/{article_id}", response_model=ArticleRead)
def get_an_article(article_id: int, db: Session = Depends(get_db)):

  db_article = get_article(db, article_id=article_id)
  if not db_article:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article non trouver")
  return db_article


"""creer un article dans la db"""
@router.post("/", response_model=ArticleRead)
def create_new_article(article: ArticleCreate, db: Session = Depends(get_db)) -> Any:

  new_article = create_article(db, article=article)
  if not new_article:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article non trouver")
  return new_article



"""supprimer un article par son id"""
@router.delete('/{article_id}')
def delete_article_by_id(article_id: Annotated[int, Path()], db: Session = Depends(get_db)):
  
  article = delete_article(db, article_id=article_id)

  if not article:
    raise HTTPException(status_code=404, detail="Article non trouver")

  return {"message": "Article supprimer"}



