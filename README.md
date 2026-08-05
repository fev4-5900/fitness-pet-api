# FitPet

[![Live Demo](https://img.shields.io/badge/FitPet-Live%20Demo-2ea44f)](https://fitness-pet-api.onrender.com)

A gamified fitness companion **backend API** — the kind of project that turns daily fitness habits (meals, water, sleep, steps) into a game where your pixel-art pet grows as you hit your targets. Try it live: **https://fitness-pet-api.onrender.com**

**This is primarily a backend project.** The FastAPI backend (auth, database, scoring engine, target calculator, logging API) is hand-built. A lightweight React frontend was added with the help of AI simply to showcase and exercise the API — the logic and data lives in the backend.

## What's in the backend

### REST API (FastAPI + SQLAlchemy + Pydantic v2)
- Modular **router architecture**: `auth`, `user`, `pet`, `targets`, `points`, plus a `logs/` subpackage for meals, water, sleep and steps
- Typed request/response models with `Annotated` dependencies (Pydantic v2 style)
- Per-router `get_db()` / `db_dependency` / `user_dependency` boilerplate
- SQLAlchemy ORM models — one table per entity (`user`, `pet`, `user_targets`, `meals`, `water`, `sleep_hours`, `steps`, `overall_points`)
- SQLite for local development, PostgreSQL via `DATABASE_URL` for production

### Authentication
- JWT (HS256, 20-minute expiry) signed with a **`SECRET_KEY` read from the environment**, never committed
- Passwords hashed with **bcrypt** (plain text is never stored)
- Server-side validation: passwords require 6+ characters, usernames/emails must be unique (duplicates return `400`)
- Every protected endpoint validates the token and ownership (returns `401` otherwise)
- **Rate limiting on login** (`slowapi`, 5 attempts/minute per IP) to block brute-force password guessing, with a friendly `429` message

### Gamification engine
- **Daily score out of 100** — calories (±200/±300 window), protein, sleep, steps and water are each graded against the user's saved targets
- **Pet mood** — `sad` / `ok` / `happy` based on the daily score
- **Lifetime points + 10 levels** — a delta-tracking system that adds only the *change* in today's score to the user's lifetime total after every log

### Targets calculator
- Science-based daily recommendations (Mifflin-St Jeor BMR → TDEE → goal-adjusted calories → macro split → water/steps goals) computed from the user's fitness profile

### Single-service deployment
- The backend serves the built React app from `frontend/dist`, so the whole project deploys as **one service** with no CORS setup

## Frontend (AI-assisted)

A small React (Vite) app — login, register, dashboard, logging and targets screens — built with the help of AI to demonstrate the API. It talks to the backend through `/api` (proxied to port 8000 in development, same-origin in production).

## Tech Stack

| Layer      | Technology                                      |
| ---------- | ----------------------------------------------- |
| Backend    | FastAPI, SQLAlchemy, Pydantic v2, python-jose, passlib/bcrypt, slowapi |
| Database   | SQLite (local) / PostgreSQL (production)        |
| Frontend   | React 19, Vite, react-router-dom (AI-assisted)  |

## Project Structure

```
fitness-pet-api/
├── backend/                  # FastAPI application (the main work)
│   ├── main.py               # App entry point (also serves the built frontend)
│   ├── config.py             # Environment-variable config (SECRET_KEY, DATABASE_URL)
│   ├── database.py           # Database engine / session setup
│   ├── models.py             # SQLAlchemy table definitions
│   ├── requirements.txt      # Pinned Python dependencies
│   ├── .env.example          # Template for environment variables
│   └── routers/
│       ├── auth.py           # Register / login / JWT handling + rate limiting
│       ├── user.py           # Fitness profile
│       ├── pet.py            # Pet CRUD (one pet per user)
│       ├── targets.py        # Recommended + saved daily targets
│       ├── points.py         # Daily score + lifetime level calculation
│       └── logs/             # meals, water, sleep, steps
└── frontend/                 # React / Vite app (AI-assisted showcase)
    ├── vite.config.js        # Dev proxy: /api -> http://localhost:8000
    └── src/
        ├── api.js            # API helper + token handling
        ├── pages/            # Login, Register, Dashboard, Log, Targets, Profile, CreatePet
        └── components/       # Chinchilla, Scene, PixelIcon, ProgressBar, Layout
```

## Getting Started

### Prerequisites

- Python 3.11+

### Run the backend

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

The API (with interactive Swagger docs) is now at `http://localhost:8000/docs`.

### Run the frontend (development only)

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. In development the Vite server proxies `/api` requests to the backend.

## Environment Variables

| Variable        | Required | Default                | Description                                     |
| --------------- | -------- | ---------------------- | ----------------------------------------------- |
| `SECRET_KEY`    | Yes      | -                      | Signs/verifies JWT tokens. Generate a long random string. |
| `DATABASE_URL`  | No       | `sqlite:///./fitness-pet.db` | Full database URL. Set to a PostgreSQL URL in production so user data survives redeploys. |

## API Reference

Interactive docs are available at `/docs`. Main endpoints:

| Method   | Path                       | Description                         |
| -------- | -------------------------- | ----------------------------------- |
| POST     | `/auth/creat_user`         | Register a new account              |
| POST     | `/auth/token`              | Login (rate-limited), returns a bearer JWT |
| GET      | `/user/profile`            | Read fitness profile                |
| PUT      | `/user/edit_profile`       | Update fitness profile              |
| GET      | `/pet/read_pet_info`       | Read your pet                       |
| POST     | `/pet/creat_pet`           | Create your pet (one per user)      |
| PUT      | `/pet/edit_pet_info`       | Edit your pet                       |
| DELETE   | `/pet/delete`              | Delete your pet                     |
| GET      | `/targets/recommended`     | Recommended targets from your profile |
| GET      | `/targets/read_targets`    | Read your saved targets             |
| POST      | `/targets/add_targets`     | Save your targets                   |
| GET      | `/points/daily`            | Today's score (out of 100) + mood   |
| GET      | `/points/total`            | Lifetime points + level             |
| POST     | `/meals/log_meals`         | Log a meal                          |
| POST     | `/water/log_water`         | Log water                           |
| POST     | `/sleep/log_sleep`         | Log sleep                           |
| POST     | `/steps/log_steps`         | Log steps                           |

Every protected endpoint expects `Authorization: Bearer <token>`.

## Deployment (Render + Neon)

The backend serves the built frontend from `frontend/dist`, so the whole project deploys as **one web service**.

1. Push this repo to GitHub and connect it to a new Render **Web Service**.
2. Set the following:

   | Setting         | Value                                       |
   | --------------- | ------------------------------------------- |
   | Build command   | `cd frontend && npm ci && npm run build`    |
   | Start command   | `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT` |
   | Runtime         | Python 3.11                                 |

3. Create a free PostgreSQL database on **Neon** (`neon.tech`), copy its connection string, and set two environment variables on the Render service:

   | Key            | Value                    |
   | -------------- | ------------------------ |
   | `SECRET_KEY`   | your random secret       |
   | `DATABASE_URL` | the Neon connection string |

Why PostgreSQL? Render's free tier wipes the server disk on every redeploy, so an SQLite file loses all user accounts each time. PostgreSQL lives on a separate server, so data survives redeploys — even if you ever move the app to another host, pointing at the same `DATABASE_URL` brings every account back.

## Security Notes

- `SECRET_KEY` and `DATABASE_URL` are read from the environment, never committed. Keep `backend/.env` out of git (it is ignored).
- Passwords are hashed with bcrypt; plain-text passwords are never stored.
- Passwords require a minimum of 6 characters; usernames/emails must be unique (duplicates return `400`).
- Login is rate-limited (5 attempts/minute per IP) against brute-force attacks.
- The database file and any `.env` files are ignored by git - never force-add them.

## License

This project is for personal/portfolio use.
