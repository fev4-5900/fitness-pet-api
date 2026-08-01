from fastapi import FastAPI
from database import engine, Base
from routers import pet, auth, user, targets, meals, exercise, sleep, water, steps

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(pet.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(targets.router)
app.include_router(meals.router)
app.include_router(exercise.router)
app.include_router(sleep.router)
app.include_router(water.router)
app.include_router(steps.router)
