from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import models, schemas, utils
# import psycopg2
# from psycopg2.extras import RealDictCursor
import time
from db import get_db
import models
import schemas
from sqlalchemy.orm import Session
import utils
import oauth2

router = APIRouter(
    prefix= "/posts",
    tags=["Posts"]
)
@router.get("/sqlalchemy")
def test_posts(db : Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    #res = db.query(models.SqaPost).all()
    res = db.query(models.SqaPost) #This actually gives SQL command
    print(res)
    print(res.all())
    return res.all()
    #return {"status":"Green"}


# @router.post("/post-comment")
# def posted_comment(payload: dict = Body(...)):
#     print(payload)
#     return {"post":f"title:{payload['title']} and content:{payload['content']}"}

#using pydentic schema
#Added 201 code because successful creation uses 201 resp code and not the default 200
@router.post("/comment", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def posted_comment(payload: schemas.Post):
    print(payload.dict())
    print(payload.rating)
    return {"post":f"{payload}"}

@router.get("/alchemy/{id}")
def get_post_byid(id: int, db:Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    res = db.query(models.SqaPost).filter(models.SqaPost.id == id).first()
    print(res)
    return {"Res":res}


@router.post("/alchemy", status_code=status.HTTP_201_CREATED)
def create_new_post(payload: schemas.Post, db:Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    #new_post = models.SqaPost(title=payload.title, content=payload.content, published=payload.publish)
    new_post = models.SqaPost(**payload.dict()) #** will unpack the dict to perform assignment like in the above commented stmt.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(user_id)
    return {"res":new_post}