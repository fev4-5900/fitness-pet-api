# FIT PET

A gamified fitness companion app. Create your own pixel-art chinchilla pet, log your meals, water, sleep and steps every day, and watch your pet grow as you hit your daily targets.

The app combines a **React (Vite)** frontend with a **FastAPI** backend. In production the backend serves the built frontend, so the whole app runs as a single service.

## Features

- **Virtual pet** - create one pixel-art chinchilla per account and keep it happy by staying on track
- **Daily targets** - science-based recommendations (calories, macros, water, sleep, steps) calculated from your profile
- **Activity log** - track meals, water, sleep and steps, one entry at a time
- **Daily score (out of 100)** - each category is graded against your targets
- **Levels** - lifetime points accumulate and level your pet up
- **Auth** - JWT login with bcrypt password hashing
- **Pixel-art UI** - cozy fireplace / library / gym theme with a custom-drawn chinchilla sprite

## Tech Stack

| Layer      | Technology                                      |
| ---------- | ----------------------------------------------- |
| Frontend   | React 19, Vite, react-router-dom                |
| Backend    | FastAPI, SQLAlchemy, Pydantic v2                |
| Database   | SQLite (local) or PostgreSQL (production)       |
| Auth       | JWT (python-jose), bcrypt (passlib)             |

## Project Structure

```
fitness-pet-api/
├── backend/                  # FastAPI application
│   ├── main.py               # App entry point (also serves the built frontend)
│   ├── config.py             # Environment-variable config (SECRET_KEY, DATABASE_URL)
│   ├── database.py           # Database engine / session setup
│   ├── models.py             # SQLAlchemy table definitions
│   ├── requirements.txt      # Pinned Python dependencies
│   ├── .env.example          # Template for environment variables
│   └── routers/
│       ├── auth.py           # Register / login / JWT handling
│       ├── user.py           # Fitness profile
│       ├── pet.py            # Pet CRUD
│       ├── targets.py        # Recommended + saved daily targets
│       ├── points.py         # Daily score + lifetime level calculation
│       └── logs/             # meals, water, sleep, steps
└── frontend/                 # React / Vite app
    ├── vite.config.js        # Dev proxy: /api -> http://localhost:8000
    └── src/
        ├── api.js            # API helper + token handling
        ├── pages/            # Login, Register, Dashboard, Log, Targets, Profile, CreatePet
        └── components/       # Chinchilla, Scene, PixelIcon, ProgressBar, Layout
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+

### 1. Run the backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate            # Windows (use `source venv/bin/activate` on macOS/Linux)
pip install -r requirements.txt
```

Create the environment file (required - the app refuses to start without `SECRET_KEY`):

```bash
copy .env.example .env           # Windows
# cp .env.example .env           # macOS/Linux
```

Open `.env` and set a real random `SECRET_KEY` (e.g. `python -c "import secrets; print(secrets.token_hex(32))"`).

Start the server:

```bash
python -m uvicorn main:app --reload --port 8000
```

The API (with interactive docs) is now at `http://localhost:8000/docs`.

### 2. Run the frontend (development)

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. In development the Vite server proxies `/api` requests to the backend, so no CORS setup is needed.

## Environment Variables

| Variable        | Required | Default                | Description                                     |
| --------------- | -------- | ---------------------- | ----------------------------------------------- |
| `SECRET_KEY`    | Yes      | -                      | Signs/verifies JWT tokens. Generate a long random string. |
| `DATABASE_URL`  | No       | `sqlite:///./fitness-pet.db` | Full database URL. Set to a PostgreSQL URL in production so data survives redeploys. |

## API Reference

Interactive docs are available at `/docs`. Main endpoints:

| Method   | Path                       | Description                         |
| -------- | -------------------------- | ----------------------------------- |
| POST     | `/auth/creat_user`         | Register a new account              |
| POST     | `/auth/token`              | Login, returns a bearer JWT         |
| GET      | `/user/profile`            | Read fitness profile                |
| PUT      | `/user/edit_profile`       | Update fitness profile              |
| GET      | `/pet/read_pet_info`       | Read your pet                       |
| POST     | `/pet/creat_pet`           | Create your pet (one per user)      |
| PUT      | `/pet/edit_pet_info`       | Edit your pet                       |
| DELETE   | `/pet/delete`              | Delete your pet                     |
| GET      | `/targets/recommended`     | Recommended targets from your profile |
| GET      | `/targets/read_targets`    | Read your saved targets             |
| POST     | `/targets/add_targets`     | Save your targets                   |
| GET      | `/points/daily`            | Today's score (out of 100) + mood   |
| GET      | `/points/total`            | Lifetime points + level             |
| POST     | `/meals/log_meals`         | Log a meal                          |
| POST     | `/water/log_water`         | Log water                           |
| POST     | `/sleep/log_sleep`         | Log sleep                           |
| POST     | `/steps/log_steps`         | Log steps                           |

Every protected endpoint expects `Authorization: Bearer <token>`.

## Deployment (Render)

The backend serves the built frontend from `frontend/dist`, so the whole app deploys as one service.

1. Push this repo to GitHub and connect it to a new Render **Web Service**.
2. Set the following:

   | Setting         | Value                                       |
   | --------------- | ------------------------------------------- |
   | Build command   | `cd frontend && npm ci && npm run build`    |
   | Start command   | `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT` |
   | Runtime         | Python 3.11                                 |
   | `SECRET_KEY`    | your random secret                          |

3. (Optional but recommended) Add a Render PostgreSQL database and set `DATABASE_URL` to its connection string, so user data survives redeploys. Without it the app uses a SQLite file on the server, which is wiped on every new deploy.

## Security Notes

- `SECRET_KEY` is read from the environment, never committed. Keep `backend/.env` out of git (it is ignored).
- Passwords are hashed with bcrypt; plain-text passwords are never stored.
- Passwords require a minimum of 6 characters and usernames/emails must be unique (duplicates return `400`).
- The database file and any `.env` files are ignored by git - never force-add them.

## License

This project is for personal/portfolio use.
