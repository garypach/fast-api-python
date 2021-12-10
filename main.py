from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content:str
    published: bool = True

@app.get("/")
async def root():
    return {"message": "Hello World2"}

@app.post("/createpost")
async def get_posts(post:Post):
    print(post.dict())
    return {"data": post.dict()}


#title str, content str