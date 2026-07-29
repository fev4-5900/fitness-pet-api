from datetime import timedelta, timezone, datetime
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from passlib.context import CryptContext

from database import SessionLocal
from models import user

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "f6837ff897fc7e8eb1746c32699f43b9"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User_Request(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/creat_user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: User_Request):
    create_user_model = user(
        username=user_request.username,
        email=user_request.email,
        hashed_password=bcrypt_context.hash(user_request.password),
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        phone_number=user_request.phone_number,
    )
    db.add(create_user_model)
    db.commit()


def authenticate_user(username: str, password: str, db):
    user_model = db.query(user).filter_by(username=username).first()
    if not user_model:
        return False
    if not bcrypt_context.verify(password, user_model.hashed_password):
        return False
    return user_model


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    expires = datetime.now(timezone.utc) + expires_delta
    encode = {"sub": username, "id": user_id, "exp": expires}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: db_dependency,):
    user_model = authenticate_user(form_data.username, form_data.password, db)
    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = create_access_token(user_model.username, user_model.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}
