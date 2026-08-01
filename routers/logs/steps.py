from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from pydantic import BaseModel, Field
from models import pet, user, user_targets, steps
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session, query
from routers.auth import get_current_user
from datetime import date
router = APIRouter(
    prefix="/steps",
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# Body expected when logging steps (date is set by the server)
class Steps_Request(BaseModel):
    steps :int


# All steps entries ever logged by this user
@router.get("/read_all_steps")
async def read_all_steps(db:db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    return db.query(steps).filter_by(owner_id = current_user.get("id")).all()


# Only today's steps entries
@router.get("/read_today_steps")
async def read_today_steps(db:db_dependency,current_user:user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    today = date.today()
    return db.query(steps).filter(steps.owner_id == current_user.get("id"),steps.date == today,).all()

# Read one specific entry (only if it belongs to this user)
@router.get("/read_steps/{steps_id}")
async def read_steps_by_id(db:db_dependency, current_user: user_dependency, steps_id:int):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    steps_model = db.query(steps).filter(steps.id == steps_id, steps.owner_id == current_user.get("id")).first()
    if steps_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Steps not found")
    return steps_model

# Total steps recorded today
@router.get("/today_totals")
async def read_today_totals(db: db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    today = date.today()
    rows = db.query(steps).filter(steps.owner_id == current_user.get("id"), steps.date == today).all()
    return {
        "steps": sum(s.steps or 0 for s in rows),
    }

# Add a new steps entry for today
@router.post("/log_steps")
async def log_steps(db:db_dependency,current_user:user_dependency, steps_request:Steps_Request):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    steps_model = steps(**steps_request.model_dump())
    steps_model.owner_id = current_user.get("id")
    steps_model.date = date.today()


    db.add(steps_model)
    db.commit()

# Remove an entry (only if it belongs to this user)
@router.delete("/delete_steps/{steps_id}")
async def delete_steps(db: db_dependency, current_user: user_dependency, steps_id: int):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    steps_model = db.query(steps).filter(steps.id == steps_id, steps.owner_id == current_user.get("id")).first()

    if steps_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Steps not found")

    db.delete(steps_model)
    db.commit()
