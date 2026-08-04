from fastapi import FastAPI
from database import engine, Base
from routers import pet, auth, user, targets, points
from routers.logs import water, sleep, meals, steps

# Create the FastAPI app (the main entry point of the API)
app = FastAPI()

# Create all database tables that don't exist yet (pet, user, targets, logs...)
Base.metadata.create_all(bind=engine)

# Register every router so its endpoints are exposed on the app
app.include_router(pet.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(targets.router)
app.include_router(points.router)
app.include_router(meals.router)
app.include_router(sleep.router)
app.include_router(water.router)
app.include_router(steps.router)
