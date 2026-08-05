# Endpoints for the user's virtual pet: create, read, edit and delete.
# Each user can only own one pet.
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


# db_dependency opens a fresh DB session per request
# user_dependency resolves the logged-in user from the token
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class Pet_Req(BaseModel):
    name: str = Field(min_length=3, max_length=50)  # pet name validation
    description: str = Field(max_length=300)
    color: str


# Read your pet info
@router.get("/read_pet_info", status_code=status.HTTP_200_OK)
async def read_pet_info(current_user: user_dependency, db: db_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    pet_model = db.query(pet).filter(pet.owner_id == current_user.get("id")).all()
    return pet_model


# Create a new pet (one per user)
@router.post("/creat_pet", status_code=status.HTTP_201_CREATED)
async def create_pet(current_user: user_dependency, db: db_dependency, pet_req: Pet_Req):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    existing_pet = db.query(pet).filter(pet.owner_id == current_user.get("id")).first()
    if existing_pet:
        raise HTTPException(status_code=400, detail="You already have a pet")

    pet_model = pet(**pet_req.model_dump())
    pet_model.owner_id = current_user.get("id")
    db.add(pet_model)
    db.commit()


# Update your pet's info
@router.put("/edit_pet_info", status_code=status.HTTP_200_OK)
async def update_pet(pet_req: Pet_Req, db: db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    pet_model = db.query(pet).filter(pet.owner_id == current_user.get("id")).first()

    if pet_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    pet_model.name = pet_req.name
    pet_model.description = pet_req.description
    pet_model.color = pet_req.color
    db.commit()


# Delete your pet
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet(current_user: user_dependency, db: db_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    pet_model = db.query(pet).filter(pet.owner_id == current_user.get("id")).first()
    if pet_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(pet_model)
    db.commit()
