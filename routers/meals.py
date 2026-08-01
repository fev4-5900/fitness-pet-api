from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from pip._internal.utils import datetime
from pydantic import BaseModel, Field
from sqlalchemy.sql.functions import now
from sqlalchemy.testing.pickleable import User
from models import pet, user, user_targets, meals
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session, query
from .auth import get_current_user
from datetime import date
router = APIRouter(
    prefix="/meals",
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class Meals_Request(BaseModel):
    calories : int
    proteins :int
    carbs : int
    fats : int


@router.get("/read_all_meals")
async def read_all_meals(db:db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    return db.query(meals).filter_by(owner_id = current_user.get("id")).all()


@router.get("/read_today_meals")
async def read_today_meals(db:db_dependency,current_user:user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    today = date.today()
    return db.query(meals).filter(meals.owner_id == current_user.get("id"),meals.date == today,).all()

@router.get("/read_meals/{meal_id}")
async def read_meals_by_id(db:db_dependency, current_user: user_dependency, meal_id:int):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    meal_model = db.query(meals).filter(meals.id == meal_id, meals.owner_id == current_user.get("id")).first()
    if meal_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")
    return meal_model

@router.get("/today_totals")
async def read_today_totals(db: db_dependency, current_user: user_dependency):
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

@router.post("/log_meals")
async def log_meals(db:db_dependency,current_user:user_dependency, meals_request:Meals_Request):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    meal_model = meals(**meals_request.model_dump())
    meal_model.owner_id = current_user.get("id")
    meal_model.date = date.today()


    db.add(meal_model)
    db.commit()

@router.delete("/delete_meal/{meal_id}")
async def delete_meal(db: db_dependency, current_user: user_dependency, meal_id: int):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    meal_model = db.query(meals).filter(meals.id == meal_id, meals.owner_id == current_user.get("id")).first()

    if meal_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")

    db.delete(meal_model)
    db.commit()







