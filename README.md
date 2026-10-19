# Priyanshu Raj — Personal Portfolio (No Docker)

A responsive portfolio built with React + Vite + TypeScript, Python FastAPI, and SQLAlchemy. Your supplied portrait is included locally at `frontend/public/priyanshu-raj.png`. Docker files have been removed.

## Requirements

- Node.js 20+ (includes npm)
- Python 3.11+
- VS Code (recommended)
- For the fastest local start, no PostgreSQL installation is needed: the API defaults to a local SQLite file. PostgreSQL is supported when you are ready to configure it.

## Run locally on Windows (PowerShell)

Open the project root in VS Code. Use two separate terminals.

### 1. Backend terminal

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
$env:DATABASE_URL="sqlite:///./portfolio.db"
$env:ADMIN_EMAIL="your-admin-email@example.com"
$env:ADMIN_PASSWORD="REPLACE_WITH_A_LONG_UNIQUE_PASSWORD"
$env:JWT_SECRET="REPLACE_WITH_A_RANDOM_SECRET_AT_LEAST_32_CHARACTERS_LONG"
$env:CORS_ORIGINS="http://localhost:5173"
uvicorn app.main:app --reload --port 8000
```

Keep this terminal open. On first startup, the API creates the SQLite database and seeds initial portfolio content. The database file is created in `backend/portfolio.db`.

If PowerShell blocks activation, run this once in the current terminal and then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 2. Frontend terminal

Open a second terminal at the project root:

```powershell
cd frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

Open the Vite URL shown in the terminal, normally `http://localhost:5173`. API docs are at `http://localhost:8000/docs`, and the health check is `http://localhost:8000/health`.

### Admin dashboard

Use the **Admin** link in the page footer or visit `http://localhost:5173/admin`. Sign in with the `ADMIN_EMAIL` and `ADMIN_PASSWORD` values you set in the backend terminal. Never use example credentials on a public deployment.

## Use PostgreSQL instead of SQLite

1. Install PostgreSQL locally and ensure its service is running.
2. Create a database named `portfolio` and a database user with a strong password.
3. In the backend terminal, replace the SQLite URL with your actual local PostgreSQL connection string, for example:

```powershell
$env:DATABASE_URL="postgresql+psycopg://portfolio:YOUR_PASSWORD@localhost:5432/portfolio"
```

4. Restart Uvicorn. The `psycopg` driver is already listed in `backend/requirements.txt`. Keep database credentials private.

## What's included

- Responsive portfolio, about, skills, projects, achievements, and contact form
- Locally stored portrait image (no external avatar dependency)
- FastAPI API and interactive Swagger docs
- SQLAlchemy persistence (SQLite by default; PostgreSQL supported)
- Contact message storage and basic rate limiting
- Admin authentication and content/message management endpoints
- Backend smoke tests

## Important profile review

Review project descriptions, role names, achievement dates, email address, DSA count, and repository links before publishing. The portfolio starter includes profile information gathered from the public GitHub profile, but you should verify that all details are current and accurate.

## Production notes

This folder is for local development. Before public deployment, configure a managed PostgreSQL database, production secrets, HTTPS, exact CORS origins, and a suitable frontend/backend hosting setup. Do not commit `.env`, passwords, database files, or private keys. Add database migrations before evolving the production schema.
