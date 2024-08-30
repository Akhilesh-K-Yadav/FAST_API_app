from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import models, schemas, utils
from db import engine, session_local, get_db
import models
import schemas
from sqlalchemy.orm import Session
import oauth2

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.SqaPost).filter(models.SqaPost.id == vote.post_id).first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{current_user.id} has already voted for {vote.post_id}")
        new_vote = models.Vote(post_id= vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit() 
        return{"message":"Successfully added vote!"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message":"Deleted vote successfully!"}
