from fastapi import FastAPI, Response,status,HTTPException
from pydantic import BaseModel
from random import randrange

from starlette.responses import Response
app = FastAPI()

class Post(BaseModel):
    title: str
    content:str
    published: bool = True

my_posts = [{"title": "title of post1", "content":"content1","id": 1},{"title": "title of post2", "content":"content2","id": 2} ]

def find_post(id:int):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello World2"}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code= status.HTTP_201_CREATED)
async def get_posts(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": post}

@app.get("/posts/{id}")
def get_post(id:int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"post with id: {id} was not found")
    return{"post_detail": post}

@app.delete("/posts/{id}")
def delete_post(id:int):
    # deleting post
    # find index of id
    # pop value from array
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"post with id: {id} was not found")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    print(post)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"post with id: {id} was not found")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}