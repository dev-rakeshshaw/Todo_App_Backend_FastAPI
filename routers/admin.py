from typing import Annotated
from fastapi import FastAPI,APIRouter,Depends, HTTPException,status,Path
from models import Todos
from database import SessionLocal
from sqlalchemy.orm import Session
from request_bodies import TodoRequest
from .auth import get_current_user,get_user_exception


router = APIRouter(
    prefix="/admin",
    tags=['admin']
    )


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo",status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):

    if user is None:
        # raise get_user_exception
        raise HTTPException(status_code=401, detail="Authentication Failed due to no user")
    
    print(user.get("user_role"))

    if user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed due to no admin")
    
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):

    if user is None:
        # raise get_user_exception
        raise HTTPException(status_code=401, detail="Authentication Failed due to no user found")
    
    print(user.get("user_role"))

    if user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed due you are not an admin")


    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "Todo not found.")
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()

    return{
    "status":201,
    'transaction':'Successful'}