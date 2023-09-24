from typing import Annotated
from fastapi import FastAPI,Depends, HTTPException,status,Path
import models 
# from models import Todos
from database import engine, SessionLocal
# from sqlalchemy.orm import Session
from request_bodies import TodoRequest
from routers.auth import get_current_user,get_user_exception
from routers import auth, todos, admin,users

app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

models.Base.metadata.create_all(bind=engine)




