from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange
app = FastAPI()

class Post(BaseModel):
    title: str
    content:str
    published: bool = True

my_posts = [{"title": "title of post1", "content":"content1","id": 1},{"title": "title of post2", "content":"content2","id": 2} ]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
async def root():
    return {"message": "Hello World2"}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts")
async def get_posts(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": post}

@app.get("/posts/{id}")
def get_post(id:int):
    post = find_post(id)
    return{"post_detail": post}


#title str, content str