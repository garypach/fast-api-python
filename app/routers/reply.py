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
    prefix="/replys",
    tags=['Replies']
)

@router.get("/{id}", response_model= List[schemas.ReplysResponseBase])
def get_comment_replys(id:int,db: Session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""" , (str(id)))
    # post = cursor.fetchone()
    comment = db.query(models.Reply).filter(models.Reply.comment_id == id).all()
    if not comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"comment with id: {id} was not found")
    return comment


#body needs title string and content post id
@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.ReplysResponseBase)
async def create_reply(reply:schemas.Replys, db: Session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    comment = db.query(models.Comment).filter(models.Comment.id == reply.comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"comment does not exist")
    
    new_reply = models.Reply(owner_id=current_user.id ,**reply.dict())
    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)
    return new_reply