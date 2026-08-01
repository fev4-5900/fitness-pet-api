from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from pydantic import BaseModel, Field
from models import pet, user, user_targets
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session, query
from .auth import get_current_user

router = APIRouter(prefix="/targets", tags=["targets"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]



class Targets_Request(BaseModel):
    calories: int
    proteins: float
    carbs: float
    fats: float
    sleep_hours:float
    steps: int



#science-based recommended targets based on the user's profile
@router.get("/recommended", status_code=status.HTTP_200_OK)
async def recommended_targets(db: db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    profile = db.query(user).filter_by(id=current_user.get("id")).first()
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    weight_kg = profile.weight
    height_cm = profile.height
    age = profile.age
    gender = profile.gender.lower() if profile.gender else ""

    # Mifflin-St Jeor BMR
    if gender == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    # Match common calorie apps: assume sedentary baseline, small adjustments
    multiplier = 1.2
    tdee = bmr * multiplier

    # Goal adjustment
    goal = profile.goal.lower() if profile.goal else "maintain"
    if goal == "lose":
        calories = tdee - 100
    elif goal == "gain":
        calories = tdee + 300
    else:
        calories = tdee

    # Macro split
    proteins = weight_kg * 1.8
    fats = calories * 0.25 / 9
    carbs = (calories - (proteins * 4 + fats * 9)) / 4

    return {
        "calories": round(calories),
        "proteins": round(proteins),
        "carbs": round(carbs),
        "fats": round(fats),
        "sleep_hours": 8,
        "steps": 10000,
    }



@router.get("/read_targets", status_code=status.HTTP_200_OK)
async def read_targets(db:db_dependency, current_user:user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    targets = db.query(user_targets).filter(user_targets.owner_id == current_user.get("id")).all()

    if targets is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User doesn't own targets")
    return targets



@router.post("/add_targets", status_code=status.HTTP_200_OK)
async def add_targets(db:db_dependency, current_user:user_dependency,target_request:Targets_Request):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    targets_model = db.query(user_targets).filter(user_targets.owner_id == current_user.get("id")).first()

    if targets_model is None:
        targets_model = user_targets(owner_id=current_user.get("id"))

    targets_model.calories = target_request.calories
    targets_model.proteins = target_request.proteins
    targets_model.carbs = target_request.carbs
    targets_model.fats = target_request.fats
    targets_model.sleep_hours = target_request.sleep_hours
    targets_model.steps = target_request.steps
    
    db.add(targets_model)
    db.commit()







