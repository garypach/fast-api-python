from fastapi import APIRouter,Depends,status,HTTPException,Response
from pydantic import utils
from sqlalchemy.orm import Session, session, util
from .. import database,schemas,models,utils,oAuth2
from ..database import engine, get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=(['Authentication'])
)

@router.post("/login", response_model=schemas.Token)
def login(response: Response,user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oAuth2.create_access_token(data = {"user_id":user.id})
    response.set_cookie(key="access_token",value=f"Bearer {access_token}", httponly=True)
    return {"access_token":access_token, "token_type":"Bearer"}


