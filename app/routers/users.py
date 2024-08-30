from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import models, schemas, utils
import psycopg2
from psycopg2.extras import RealDictCursor
from db import engine, session_local, get_db
import models
import schemas
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UsersCreateResp)
def create_user(user: schemas.CreateUsers, db:Session = Depends(get_db)):
    user.password = utils.hash_pwd(user.password)
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    