from fastapi import FastAPI, Response,status,HTTPException,APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from userpass import user
from userpass import password
from .. import models,schemas,utils
from ..database import engine, get_db
from typing import Optional, List

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/users",
    tags=['Users']
)



@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.UserOut)
async def post_posts(user:schemas.UserCreate, db: Session = Depends(get_db)):
    
    #hashpassword
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model= schemas.UserOut)
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with id: {id} was not found")
    return user