from fastapi import FastAPI, Response,status,HTTPException
from fastapi.params import Depends
from fastapi.routing import APIRouter
from pydantic import BaseModel
from random import randrange
import psycopg2
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_403_FORBIDDEN
from app import oAuth2
from userpass import user
from userpass import password
import time
from .. import models,schemas,utils,oAuth2
from ..database import engine, get_db
from typing import Optional, List
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


class Post(BaseModel):
    title: str
    content:str
    published: bool = True

# while True:
#     try:
#         conn = psycopg2.connect(host="localhost",database='fastapi database',user=user,password=password, cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print ("Error: ", error)
#         time.sleep(3)



# my_posts = [{"title": "title of post1", "content":"content1","id": 1},{"title": "title of post2", "content":"content2","id": 2} ]


# def find_post(id:int):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

@router.get("/",  response_model= List [schemas.ResponseBase])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.ResponseBase)
async def create_posts(post:Post, db: Session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    print( current_user)
    new_post = models.Post(owner_id=current_user.id ,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}")
def get_post(id:int,db: Session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""" , (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"post with id: {id} was not found")
    return post

@router.delete("/{id}")
def delete_post(id:int,db: Session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user)):
    # deleting post
    # find index of id
    # pop value from array
    # index = find_index_post(id)
    # cursor.execute("""DELETE from posts WHERE id = %s RETURNING *""" , (str(id)))
    # delete_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action") 
    
    post_query.delete(synchronize_session=False)

    db.commit()

@router.put("/{id}")
def update_post(id:int, post: Post,db: Session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""" , (post.title,post.content,post.published,str(id)))
    # updated_post =  cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"post with id: {id} was not found")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action") 

    post_query.update(post.dict(),synchronize_session=False)

    db.commit()
    
    return post_query.first()
