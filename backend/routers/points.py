from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from pydantic import BaseModel, Field
from models import pet, user, user_targets, meals, sleep_hours, steps, water, overall_points
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session, query
from routers.auth import get_current_user
from datetime import date

router = APIRouter(prefix="/points", tags=["points"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# Points earned per target category (100 total)
POINTS = {
    "calories": 25,  # within ±200 of target = 30, within ±300 = 15, otherwise 0
    "proteins": 25,  # earned when protein intake reaches the target
    "sleep": 20,     # earned when sleep hours reach the target
    "steps": 15,     # earned when steps reach the target
    "water": 15,     # earned when liters of water reach the target
}


def calculate_level(total_points: int) -> int:
    thresholds = [500, 1000, 2000, 3000, 5000, 7500, 10000, 12500, 15000]

    for level, threshold in enumerate(thresholds, start=1):
        if total_points <= threshold:
            return level

    return 10





# Score one day's logs against the targets (out of 100)
def calculate_daily_points(db, user_id, target_day):
    # If the user never saved targets, there is nothing to score against
    targets = db.query(user_targets).filter_by(owner_id=user_id).first()
    if targets is None:
        return {"points": 0, "effect": "sad", "breakdown": {}}

    # Totals from each log table for that day
    calories = sum(m.calories or 0 for m in db.query(meals).filter(meals.owner_id == user_id, meals.date == target_day).all())
    proteins = sum(m.proteins or 0 for m in db.query(meals).filter(meals.owner_id == user_id, meals.date == target_day).all())
    sleep = sum(s.sleep_hours or 0 for s in db.query(sleep_hours).filter(sleep_hours.owner_id == user_id, sleep_hours.date == target_day).all())
    steps_total = sum(st.steps or 0 for st in db.query(steps).filter(steps.owner_id == user_id, steps.date == target_day).all())
    liters = sum(w.liters or 0 for w in db.query(water).filter(water.owner_id == user_id, water.date == target_day).all())

    # Calories score in a range around the target:
    # within ±200 -> full points, within ±300 -> half points, otherwise none
    cal_target = targets.calories or 0
    cal_diff = abs(calories - cal_target)
    if cal_diff <= 200:
        cal_points = POINTS["calories"]
    elif cal_diff <= 300:
        cal_points = POINTS["calories"] // 2
    else:
        cal_points = 0

    # All-or-nothing credit per category
    breakdown = {
        "calories": cal_points,
        "proteins": POINTS["proteins"] if proteins >= (targets.proteins or 0) else 0,
        "sleep": POINTS["sleep"] if sleep >= (targets.sleep_hours or 0) else 0,
        "steps": POINTS["steps"] if steps_total >= (targets.steps or 0) else 0,
        "water": POINTS["water"] if liters >= (targets.water or 0) else 0,
    }

    points = sum(breakdown.values())

    # Pet's mood for the day based on the score
    if points < 70:
        effect = "sad"
    elif points < 90:
        effect = "ok"
    else:
        effect = "happy"

    return {"points": points, "effect": effect, "breakdown": breakdown}


# Called by every log endpoint after saving a log.
# Adds the change in today's score to the lifetime total.
def sync_total_after_log(db, user_id, old_today_points):
    new_today_points = calculate_daily_points(db, user_id, date.today())["points"]
    delta = new_today_points - old_today_points

    if delta != 0:
        total = db.query(overall_points).filter(overall_points.owner_id == user_id).first()
        if total is None:
            db.add(overall_points(owner_id=user_id, overall_points=delta))
        else:
            total.overall_points += delta
        db.commit()



# Today's score + mood (live, resets automatically every day)
@router.get("/daily", status_code=status.HTTP_200_OK)
async def read_daily_points(db: db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    result = calculate_daily_points(db, current_user.get("id"), date.today())
    return {"date": date.today(), **result}


# Lifetime score (pure read)
@router.get("/total", status_code=status.HTTP_200_OK)
async def read_total_points_and_level(db: db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

    total = db.query(overall_points).filter(overall_points.owner_id == current_user.get("id")).first()

    level = calculate_level(total.overall_points if total else 0)

    return {"total_points": total.overall_points if total else 0, "level":level}


