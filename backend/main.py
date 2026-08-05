# FastAPI app entry point.
# Registers every router and, when the frontend has been built,
# serves the React app from frontend/dist on the same server.
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routers import pet, auth, user, targets, points
from routers.logs import water, sleep, meals, steps
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


# Create the FastAPI app (the main entry point of the API)
app = FastAPI()

# Rate limiting - blocks brute-force password guessing on the login endpoint.
# Keyed by the visitor's IP address.
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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

# Serve the built React app (frontend/dist) from the same server in production.
# In development the Vite dev server (port 5173) proxies /api to this backend,
# so the app works both ways without any CORS setup.
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        return FileResponse(FRONTEND_DIST / "index.html")
