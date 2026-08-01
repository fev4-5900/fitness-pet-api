from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from pydantic import BaseModel, Field
from models import pet, user, user_targets, sleep_hours
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session, query
from .auth import get_current_user
from datetime import date
router = APIRouter(
    prefix="/sleep",
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class Sleep_Request(BaseModel):
    sleep_hours :float


@router.get("/read_all_sleep")
async def read_all_sleep(db:db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    return db.query(sleep_hours).filter_by(owner_id = current_user.get("id")).all()


@router.get("/read_today_sleep")
async def read_today_sleep(db:db_dependency,current_user:user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    today = date.today()
    return db.query(sleep_hours).filter(sleep_hours.owner_id == current_user.get("id"),sleep_hours.date == today,).all()

@router.get("/read_sleep/{sleep_id}")
async def read_sleep_by_id(db:db_dependency, current_user: user_dependency, sleep_id:int):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    sleep_model = db.query(sleep_hours).filter(sleep_hours.id == sleep_id, sleep_hours.owner_id == current_user.get("id")).first()
    if sleep_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sleep not found")
    return sleep_model

@router.get("/today_totals")
async def read_today_totals(db: db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    today = date.today()
    rows = db.query(sleep_hours).filter(sleep_hours.owner_id == current_user.get("id"), sleep_hours.date == today).all()
    return {
        "sleep_hours": sum(s.sleep_hours or 0 for s in rows),
    }

@router.post("/log_sleep")
async def log_sleep(db:db_dependency,current_user:user_dependency, sleep_request:Sleep_Request):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    sleep_model = sleep_hours(**sleep_request.model_dump())
    sleep_model.owner_id = current_user.get("id")
    sleep_model.date = date.today()


    db.add(sleep_model)
    db.commit()

@router.delete("/delete_sleep/{sleep_id}")
async def delete_sleep(db: db_dependency, current_user: user_dependency, sleep_id: int):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    sleep_model = db.query(sleep_hours).filter(sleep_hours.id == sleep_id, sleep_hours.owner_id == current_user.get("id")).first()

    if sleep_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sleep not found")

    db.delete(sleep_model)
    db.commit()
