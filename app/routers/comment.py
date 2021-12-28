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

#get all comments for a post
@router.get("/{id}",  response_model= List[schemas.CommentsResponseBase])
async def get_comments(id:int, db: Session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user), limit:int = 5, skip:int = 0, search: Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    results = db.query(models.Comment).filter(models.Comment.post_id == id).limit(limit).all()
    return results


@router.get("/comment/{id}", response_model= schemas.CommentsResponseBase)
def get_one_comment(id:int,db: Session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""" , (str(id)))
    # post = cursor.fetchone()
    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"comment with id: {id} was not found")
    return comment

#body needs title string and content post id
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

@router.put("/{id}")
def update_post(id:int, comment: schemas.Comments,db: Session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""" , (post.title,post.content,post.published,str(id)))
    # updated_post =  cursor.fetchone()
    # conn.commit()
    comment_query = db.query(models.Comment).filter(models.Comment.id == id)
    updated_comment = comment_query.first()
    if updated_comment == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"post with id: {id} was not found")
    
    if updated_comment.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action") 

    comment_query.update(comment.dict(),synchronize_session=False)

    db.commit()
    
    return comment_query.first()

@router.delete("/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user)):
    # deleting post
    # find index of id
    # pop value from array
    # index = find_index_post(id)
    # cursor.execute("""DELETE from posts WHERE id = %s RETURNING *""" , (str(id)))
    # delete_post = cursor.fetchone()
    # conn.commit()
    comment_query = db.query(models.Comment).filter(models.Comment.id == id)
    comment = comment_query.first()
    if comment == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"post with id: {id} was not found")

    if comment.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action") 
    
    comment_query.delete(synchronize_session=False)

    db.commit()