# Priyanshu Raj — Personal Portfolio

<p align="center">
  <strong>A modern, full-stack developer portfolio built to showcase projects, technical skills, achievements, and professional experience.</strong>
</p>

<p align="center">
  <a href="https://github.com/Priyanshu87571">GitHub</a> •
  <a href="https://www.linkedin.com/in/priyanshu-raj-162763306/">LinkedIn</a> •
  <a href="http://localhost:5173">Local Demo</a>
</p>

---

## Overview

This repository contains my personal portfolio website, built with **React, TypeScript, Python FastAPI, and SQLAlchemy**.

The application combines a responsive frontend with a REST API backend and a database-backed content management system. Visitors can explore my projects, technical skills, education, and achievements, or contact me through the website. An authenticated admin dashboard supports project management and contact message review.

The application runs locally without Docker. SQLite is the default development database, and PostgreSQL is supported through configuration.

## Features

- **Responsive portfolio:** Modern dark-themed interface with lime-green accents, designed for desktop and mobile screens.
- **Personal profile:** Introduction, education, technical interests, and professional links.
- **Project showcase:** Display projects, technology stacks, GitHub links, and live demos.
- **Skills and achievements:** Organize technical skills and professional milestones.
- **Contact form:** Submit and persist visitor messages through the backend API.
- **Admin dashboard:** Authenticate, add projects, and review contact messages.
- **REST API:** Structured endpoints for profile information, projects, skills, achievements, authentication, and contact submissions.
- **Database persistence:** SQLAlchemy supports SQLite for local development and PostgreSQL for configured environments.
- **API documentation:** Interactive Swagger UI powered by FastAPI.
- **Local profile image:** The portfolio portrait is stored in the frontend project.

## Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite |
| Backend | Python, FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite / PostgreSQL |
| Authentication | JWT-based authentication |
| API documentation | OpenAPI, Swagger UI |
| Development tools | Git, GitHub, VS Code |

## Architecture

```text
Visitor / Admin
      |
      v
React + TypeScript + Vite
      |
      | HTTP / JSON
      v
Python FastAPI REST API
      |
      +---- Authentication
      |
      +---- Portfolio and Contact Services
      |
      v
SQLAlchemy ORM
      |
      v
SQLite / PostgreSQL
```

## Project Structure

```text
priyanshu-portfolio/
├── frontend/
│   ├── public/
│   │   └── priyanshu-raj.png
│   ├── src/
│   ├── .env.example
│   └── package.json
│
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── requirements.txt
│   └── tests/
│
├── .gitignore
└── README.md
```

*The tree above highlights the main components; exact files may vary by version.*

## Getting Started

Follow these instructions to run the project locally on Windows.

### Prerequisites

Install the following:

- [Node.js](https://nodejs.org/) with npm
- [Python](https://www.python.org/downloads/) 3.11 or later
- [Git](https://git-scm.com/)
- [Visual Studio Code](https://code.visualstudio.com/) (recommended)

You do not need Docker or a separate PostgreSQL installation for the default SQLite development setup.

### 1. Clone the repository

```powershell
git clone https://github.com/Priyanshu87571/priyanshu-portfolio.git
cd priyanshu-portfolio
```

### 2. Configure and start the backend

Open a terminal in the project root:

```powershell
cd backend

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Configure the environment variables in the same PowerShell terminal:

```powershell
$env:DATABASE_URL = "sqlite:///./portfolio.db"
$env:ADMIN_EMAIL = "your-admin-email@example.com"
$env:ADMIN_PASSWORD = "REPLACE_WITH_A_STRONG_UNIQUE_PASSWORD"
$env:JWT_SECRET = python -c "import secrets; print(secrets.token_urlsafe(48))"
$env:CORS_ORIGINS = "http://localhost:5173"
```

Replace the example admin email and password with your own values. Keep all secrets private.

Start the API:

```powershell
uvicorn app.main:app --reload --port 8000
```

Keep this terminal open while developing. The database file is created locally when the application initializes, according to its database configuration.

If PowerShell blocks virtual environment activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Configure and start the frontend

Open a second terminal in the project root:

```powershell
cd frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

Open the local URL printed by Vite, normally:

**http://localhost:5173**

### 4. Open the API documentation

Once the backend is running, use the following endpoints:

| Resource | URL |
|---|---|
| Portfolio website | http://localhost:5173 |
| Admin dashboard | http://localhost:5173/admin |
| FastAPI Swagger UI | http://localhost:8000/docs |
| OpenAPI schema | http://localhost:8000/openapi.json |
| Health check | http://localhost:8000/health |

Sign in to the admin dashboard with the credentials configured for the backend.

## PostgreSQL Configuration

SQLite is convenient for local development. To use PostgreSQL instead:

1. Install PostgreSQL locally or provision a PostgreSQL database.
2. Create a database and a dedicated database user.
3. Configure `DATABASE_URL` using your actual connection details.

Example for a local PostgreSQL installation:

```powershell
$env:DATABASE_URL = "postgresql+psycopg://portfolio:YOUR_PASSWORD@localhost:5432/portfolio"
```

Restart the backend after updating the configuration.

**Important:** Keep database credentials out of source control. For production, use a managed database, environment-based secrets, and a deliberate schema migration strategy.

## API Overview

The application exposes endpoints for the following resources:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check service and database health |
| GET | `/api/profile` | Retrieve profile information |
| GET | `/api/projects` | Retrieve portfolio projects |
| GET | `/api/skills` | Retrieve technical skills |
| GET | `/api/achievements` | Retrieve achievements |
| POST | `/api/contact` | Submit a contact message |
| POST | `/api/auth/login` | Authenticate an admin |

Additional administrative endpoints may be available in the interactive API documentation.

Open [Swagger UI](http://localhost:8000/docs) while the backend is running to inspect request schemas and test endpoints.

## Security Considerations

- Never commit `.env` files, passwords, JWT secrets, or private keys.
- Use a strong, unique admin password.
- Keep administrative endpoints protected by server-side authentication and authorization.
- Validate user input and apply appropriate rate limits to public endpoints.
- Restrict CORS to the frontend origins you actually use.
- Use HTTPS and managed secrets in production.
- Do not rely on frontend route protection alone to secure admin operations.

## Roadmap

- [ ] Deploy the frontend and backend to public hosting.
- [ ] Configure a production PostgreSQL database.
- [ ] Add automated backend and frontend tests.
- [ ] Add database migrations.
- [ ] Configure a custom domain and HTTPS.
- [ ] Add verified project demos and a downloadable resume.

## About Me

I'm Priyanshu Raj, a Computer Science and Design undergraduate interested in software engineering, full-stack development, data structures and algorithms, backend systems, and AI-powered applications.

I enjoy building practical applications and continuously improving my development and problem-solving skills.

- **GitHub:** [Priyanshu87571](https://github.com/Priyanshu87571)
- **LinkedIn:** [Priyanshu Raj](https://www.linkedin.com/in/priyanshu-raj-162763306/)

---

*Built with React, TypeScript, Python, and FastAPI.*
