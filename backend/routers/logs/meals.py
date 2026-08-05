# Meal logging: record, read and delete meals.
# Every meal is stamped with today's date by the server.
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from pip._internal.utils import datetime
from pydantic import BaseModel, Field
from sqlalchemy.sql.functions import now
from sqlalchemy.testing.pickleable import User
from models import pet, user, user_targets, meals
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session, query
from routers.auth import get_current_user
from routers.points import calculate_daily_points, sync_total_after_log
from datetime import date
router = APIRouter(
    prefix="/meals", tags=["meals"]
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# Body expected when logging a meal (the date is set automatically by the server)
class Meals_Request(BaseModel):
    calories : int
    proteins :int
    carbs : int
    fats : int


# All meals ever logged by this user
@router.get("/read_all_meals")
async def read_all_meals(db:db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    return db.query(meals).filter_by(owner_id = current_user.get("id")).all()


# Only today's meals ("reset" happens naturally via the date filter)
@router.get("/read_today_meals")
async def read_today_meals(db:db_dependency,current_user:user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    today = date.today()
    return db.query(meals).filter(meals.owner_id == current_user.get("id"),meals.date == today,).all()

# Read one specific meal (only if it belongs to this user)
@router.get("/read_meal/{meal_id}")
async def read_meal_by_id(db:db_dependency, current_user: user_dependency, meal_id:int):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    meal_model = db.query(meals).filter(meals.id == meal_id, meals.owner_id == current_user.get("id")).first()
    if meal_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")
    return meal_model

# Sum of today's meals - what the UI compares against the daily targets
@router.get("/today_total_macros")
async def read_today_total_macros(db: db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    today = date.today()
    rows = db.query(meals).filter(meals.owner_id == current_user.get("id"), meals.date == today).all()
    return {
        "calories": sum(m.calories or 0 for m in rows),
        "proteins": sum(m.proteins or 0 for m in rows),
        "carbs": sum(m.carbs or 0 for m in rows),
        "fats": sum(m.fats or 0 for m in rows),
    }

# Add a new meal for today
@router.post("/log_meals")
async def log_meals(db:db_dependency,current_user:user_dependency, meals_request:Meals_Request):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    # Today's score before this meal (to add only the change to the total)
    old_today = calculate_daily_points(db, current_user.get("id"), date.today())["points"]

    meal_model = meals(**meals_request.model_dump())
    meal_model.owner_id = current_user.get("id")
    meal_model.date = date.today()


    db.add(meal_model)
    db.commit()

    # Add the gained points (delta) to the lifetime total
    sync_total_after_log(db, current_user.get("id"), old_today)

# Remove a meal (only if it belongs to this user)
@router.delete("/delete_meal/{meal_id}")
async def delete_meal(db: db_dependency, current_user: user_dependency, meal_id: int):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    meal_model = db.query(meals).filter(meals.id == meal_id, meals.owner_id == current_user.get("id")).first()

    if meal_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")

    db.delete(meal_model)
    db.commit()







