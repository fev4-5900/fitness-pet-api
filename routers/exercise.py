from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from pydantic import BaseModel, Field
from models import pet, user, user_targets, exercise
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session, query
from .auth import get_current_user
from datetime import date
router = APIRouter(
    prefix="/exercise",
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class Exercise_Request(BaseModel):
    exercise_type : str
    duration :int
    calories_burned : int


@router.get("/read_all_exercises")
async def read_all_exercises(db:db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    return db.query(exercise).filter_by(owner_id = current_user.get("id")).all()


@router.get("/read_today_exercises")
async def read_today_exercises(db:db_dependency,current_user:user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    today = date.today()
    return db.query(exercise).filter(exercise.owner_id == current_user.get("id"),exercise.date == today,).all()

@router.get("/read_exercises/{exercise_id}")
async def read_exercises_by_id(db:db_dependency, current_user: user_dependency, exercise_id:int):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    exercise_model = db.query(exercise).filter(exercise.id == exercise_id, exercise.owner_id == current_user.get("id")).first()
    if exercise_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return exercise_model

@router.get("/today_totals")
async def read_today_totals(db: db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    today = date.today()
    rows = db.query(exercise).filter(exercise.owner_id == current_user.get("id"), exercise.date == today).all()
    return {
        "duration": sum(e.duration or 0 for e in rows),
        "calories_burned": sum(e.calories_burned or 0 for e in rows),
    }

@router.post("/log_exercise")
async def log_exercise(db:db_dependency,current_user:user_dependency, exercise_request:Exercise_Request):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    exercise_model = exercise(**exercise_request.model_dump())
    exercise_model.owner_id = current_user.get("id")
    exercise_model.date = date.today()


    db.add(exercise_model)
    db.commit()

@router.delete("/delete_exercise/{exercise_id}")
async def delete_exercise(db: db_dependency, current_user: user_dependency, exercise_id: int):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    exercise_model = db.query(exercise).filter(exercise.id == exercise_id, exercise.owner_id == current_user.get("id")).first()

    if exercise_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")

    db.delete(exercise_model)
    db.commit()
