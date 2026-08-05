# Loads app configuration from environment variables.
# In development it reads backend/.env; in production the hosting
# provider supplies the variables directly.
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./fitness-pet.db")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not set. Add it to backend/.env or set the SECRET_KEY environment variable."
    )
