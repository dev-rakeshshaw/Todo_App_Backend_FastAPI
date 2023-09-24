from typing import Annotated
from fastapi import FastAPI,APIRouter,Depends, HTTPException,status,Path,Request
from models import Todos
from database import SessionLocal
from sqlalchemy.orm import Session
from request_bodies import TodoRequest
from .auth import get_current_user,get_user_exception
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates


router = APIRouter()

# templates = Jinja2Templates(directory="templates")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# @router.get("/test_todo")
# def test_todo():
#     return{"message":"Todo files has been modified"}


#Modified: To read all the todo from the database
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency,db: db_dependency):

    if user is None:
        raise get_user_exception
    
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()



#Modified: To Create/Insert a todo in the database.
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,
                      db: db_dependency, 
                      todo_request:TodoRequest):
    
    if user is None:
        raise get_user_exception()
    
    todo_model = Todos(**dict(todo_request),owner_id = user.get("id"))

    db.add(todo_model)
    db.commit()

    return{
        "status":201,
        'transaction':'Successful'
    }



#Modified: To read particular todo from the database
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db:db_dependency, todo_id: int = Path(gt=0)):
    
    if user is None:
        raise get_user_exception
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()

    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "Todo not found.")



#Modified: To update a todo in the database
@router.put("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(user: user_dependency,
                      db: db_dependency, 
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    
    if user is None:
        raise get_user_exception()
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()
    
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "Todo not found.")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

    return{
        "status":200,
        'transaction':'Successful'}



#Modified: To delete Todo from the database
# @router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
@router.delete("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):

    if user is None:
        raise get_user_exception()

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()

    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "Todo not found.")
    
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).delete()
    db.commit()

    return{
    "status":201,
    'transaction':'Successful'}
    



