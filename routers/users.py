from typing import Annotated
from fastapi import FastAPI,APIRouter,Depends, HTTPException,status,Path
from models import Users
from database import SessionLocal
from sqlalchemy.orm import Session
from request_bodies import TodoRequest,UserVerification
from .auth import get_current_user,get_user_exception
from passlib.context import CryptContext


router = APIRouter(
    prefix="/user",
    tags=["user"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise get_user_exception
    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    
    if user is None:
        raise get_user_exception
    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if not bcrypt_context.verify(user_verification.password,user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Error on password change.")
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()