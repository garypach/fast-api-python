from fastapi import FastAPI, Response,status,HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from sqlalchemy.orm.session import Session
from app import schemas
from userpass import user
from userpass import password
from starlette.responses import Response
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas,utils
from .database import engine, get_db
from typing import Optional, List
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

@app.get("/")
async def root():
    return {"message": "Hello World2"}

@app.get("/posts",  response_model= List [schemas.ResponseBase])
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code= status.HTTP_201_CREATED, response_model= schemas.ResponseBase)
async def post_posts(post:Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}")
def get_post(id:int,db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""" , (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"post with id: {id} was not found")
    return post

@app.delete("/posts/{id}")
def delete_post(id:int,db: Session = Depends(get_db)):
    # deleting post
    # find index of id
    # pop value from array
    # index = find_index_post(id)
    # cursor.execute("""DELETE from posts WHERE id = %s RETURNING *""" , (str(id)))
    # delete_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"post with id: {id} was not found")

    post.delete(synchronize_session=False)
    db.commit()

@app.put("/posts/{id}")
def update_post(id:int, post: Post,db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""" , (post.title,post.content,post.published,str(id)))
    # updated_post =  cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"post with id: {id} was not found")
    
    post_query.update(post.dict(),synchronize_session=False)

    db.commit()
    
    return post_query.first()

@app.post("/users", status_code= status.HTTP_201_CREATED, response_model= schemas.UserOut)
async def post_posts(user:schemas.UserCreate, db: Session = Depends(get_db)):
    
    #hashpassword
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user