from fastapi import FastAPI, Response,status,HTTPException,APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import user
from .. import schemas, database, models,oAuth2
from ..database import engine, get_db

router = APIRouter(
    prefix="/commentvotes",
    tags=['Vote on comments']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def commentvote(commentvote:schemas.CommentVote,db: Session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == commentvote.comment_id).first()
    
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"comment does not exist")
    
    commentvote_query = db.query(models.CommentVote).filter(models.CommentVote.comment_id == commentvote.comment_id,models.CommentVote.user_id == current_user.id )
    found_commentvote = commentvote_query.first()
    if(commentvote.dir == 1):
        if found_commentvote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {commentvote.comment_id}")
        new_commentvote = models.CommentVote(comment_id = commentvote.comment_id, user_id = current_user.id)
        db.add(new_commentvote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_commentvote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote does not exist")

        commentvote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
