from typing import Annotated
from fastapi import FastAPI, APIRouter, Depends, HTTPException,status
from request_bodies import CreateUserRequest,Token
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal,engine
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt,JWTError

SECRET_KEY = "145192a8-0294-4ad3-a458-305d7657fde6"
ALGORITHM = "HS256"


bcrypt_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


router = APIRouter(
    prefix="/auth",
    tags=['auth']
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]



#Modified
def authenticate_user(username: str, password: str, db):

    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user



#Modified
def create_access_token(username: str, 
                        user_id: int,
                        role: str,
                        expires_delta: timedelta | None = None ):

    encode = {"sub": username, "id": user_id, "role": role}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else: 
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp":expire})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None:
            # raise get_user_exception()
            raise get_user_exception()
        return{"username": username, "id":user_id, "user_role":user_role}
    except JWTError:
        raise get_user_exception()



#modified
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency, 
                      create_user_request: CreateUserRequest 
                      ):
    create_user_model = Users(
            email = create_user_request.email,
            username = create_user_request.username,
            first_name = create_user_request.first_name,
            last_name = create_user_request.last_name,
            hashed_password = bcrypt_context.hash(create_user_request.password),
            is_active = True,
            role = create_user_request.role
    )

    db.add(create_user_model)
    db.commit()


#Modified
@router.post("/token", response_model=Token)
async def login_for_acccess_token(from_data: Annotated[OAuth2PasswordRequestForm,Depends()],db: db_dependency):
    
    user = authenticate_user(from_data.username, from_data.password, db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username,user.id,user.role,expires_delta=token_expires)

    return {"access_token":token, "token_type":"bearer"}



# Exception
def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}  # Enclose headers in braces
    )
    return credentials_exception

def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}  # Enclose headers in braces
    )
    return token_exception_response