from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from db import get_db
from schemas import UserLogin, Token
import models, utils
from oauth2 import create_token
from fastapi.security import OAuth2PasswordRequestForm

router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=Token)
#def login(user_creds: UserLogin, db: Session = Depends(get_db)):
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_creds.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid creds")
     
    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid creds")
    
    token = create_token({"user_id":user.id})
    return {"token":token, "token_type":"bearer"}