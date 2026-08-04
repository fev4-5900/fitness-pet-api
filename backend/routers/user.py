from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from pydantic import BaseModel, Field
from models import user
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user



router = APIRouter(prefix="/user", tags=["user"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]


# Body expected when editing the fitness profile
class Profile_Request(BaseModel):
    height: float
    weight: float
    age: float
    gender: str
    activity: int  # training days per week (0-7)
    goal: str  # lose / maintain / gain


# Update the logged-in user's fitness profile (used by the targets calculator)
@router.put("/edit_profile", status_code=status.HTTP_202_ACCEPTED)
async def edit_profile(db: db_dependency, current_user: user_dependency, profile_request: Profile_Request):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    profile_model = db.query(user).filter_by(id=current_user.get("id")).first()

    profile_model.height = profile_request.height
    profile_model.weight = profile_request.weight
    profile_model.age = profile_request.age
    profile_model.gender = profile_request.gender
    profile_model.activity = profile_request.activity
    profile_model.goal = profile_request.goal

    db.add(profile_model)
    db.commit()

@router.get("/profile", status_code=status.HTTP_200_OK)
async def read_profile(current_user: user_dependency, db: db_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    profile_model= db.query(user).filter_by(id=current_user.get("id")).first()

    return {"gender":profile_model.gender, "height" :profile_model.height, "weight":profile_model.weight,
            "age":profile_model.age, "goal":profile_model.goal, "activity":profile_model.activity}
