from fastapi import FastAPI, Response,status,HTTPException

from . import models,schemas,utils
from .database import engine, get_db
from .routers import posts, users,auth,vote,comment,reply,comment_vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

from app import database



# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(comment.router)
app.include_router(reply.router)
app.include_router(comment_vote.router)






@app.get("/")
async def root():
    return {"message": "Hello World Deployed from CI/CD pipeline"}
