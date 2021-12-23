from fastapi import FastAPI, Response,status,HTTPException
from fastapi.params import Depends
from fastapi.routing import APIRouter
from pydantic import BaseModel
from random import randrange
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func, mode
from starlette.status import HTTP_403_FORBIDDEN
from app import oAuth2
from sqlalchemy import func
from .. import models,schemas,utils,oAuth2
from ..database import engine, get_db
from typing import Optional, List
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

router = APIRouter(
    prefix="/comments",
    tags=['Comments']
)

@router.get("/",  response_model= List[schemas.CommentsResponseBase])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user), limit:int = 10, skip:int = 0, search: Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    results = db.query(models.Comment).all()
    
    return results

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.CommentsResponseBase)
async def create_comment(comment:schemas.Comments, db: Session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    print( current_user)
    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post does not exist")
    
    new_comment = models.Comment(owner_id=current_user.id ,**comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment