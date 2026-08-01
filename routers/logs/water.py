from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from pydantic import BaseModel, Field
from models import pet, user, user_targets, water
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session, query
from routers.auth import get_current_user
from datetime import date
router = APIRouter(
    prefix="/water",
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# Body expected when logging water (date is set by the server)
class Water_Request(BaseModel):
    liters :float


# All water entries ever logged by this user
@router.get("/read_all_water")
async def read_all_water(db:db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    return db.query(water).filter_by(owner_id = current_user.get("id")).all()


# Only today's water entries
@router.get("/read_today_water")
async def read_today_water(db:db_dependency,current_user:user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    today = date.today()
    return db.query(water).filter(water.owner_id == current_user.get("id"),water.date == today,).all()

# Read one specific entry (only if it belongs to this user)
@router.get("/read_water/{water_id}")
async def read_water_by_id(db:db_dependency, current_user: user_dependency, water_id:int):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    water_model = db.query(water).filter(water.id == water_id, water.owner_id == current_user.get("id")).first()
    if water_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Water not found")
    return water_model

# Total liters recorded today
@router.get("/today_totals")
async def read_today_totals(db: db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    today = date.today()
    rows = db.query(water).filter(water.owner_id == current_user.get("id"), water.date == today).all()
    return {
        "liters": sum(w.liters or 0 for w in rows),
    }

# Add a new water entry for today
@router.post("/log_water")
async def log_water(db:db_dependency,current_user:user_dependency, water_request:Water_Request):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    water_model = water(**water_request.model_dump())
    water_model.owner_id = current_user.get("id")
    water_model.date = date.today()


    db.add(water_model)
    db.commit()

# Remove an entry (only if it belongs to this user)
@router.delete("/delete_water/{water_id}")
async def delete_water(db: db_dependency, current_user: user_dependency, water_id: int):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    water_model = db.query(water).filter(water.id == water_id, water.owner_id == current_user.get("id")).first()

    if water_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Water not found")

    db.delete(water_model)
    db.commit()
