from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from pydantic import BaseModel, Field
from models import pet
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user

router = APIRouter(prefix="/pet", tags=["pet"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class Pet_Req(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: str = Field(max_length=300)
    color: str


@router.get("/read_pet_info", status_code=status.HTTP_200_OK)
async def read_pet_info(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    pet_model = db.query(pet).filter(pet.owner_id == user.get("id")).all()
    return pet_model


@router.post("/creat_pet", status_code=status.HTTP_201_CREATED)
async def create_pet(user: user_dependency, db: db_dependency, pet_req: Pet_Req):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    pet_model = pet(**pet_req.model_dump())
    pet_model.owner_id = user.get("id")
    db.add(pet_model)
    db.commit()


@router.put("/pet_info", status_code=status.HTTP_200_OK)
async def update_pet(pet_req: Pet_Req, db: db_dependency):
    pass
