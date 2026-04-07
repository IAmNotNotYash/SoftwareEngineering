# _Kala_ — Multi-Vendor Catalogue Marketplace Platform

A narrative-driven marketplace where independent creators (**Artists**) sell handcrafted products by telling the story behind them. Buyers can follow Artists, browse **Stories** (presentation-style catalogues), and place orders.

---

## Team

| Member | Role | Responsibilities |
|--------|------|-----------------|
| Member 1 | Backend | Flask APIs, PostgreSQL schema, authentication, artist-side APIs |
| Member 2 | Backend | Buyer & admin APIs, AI integration, pytest test cases, YAML docs |
| Member 3 | Frontend | Artist-side Vue.js pages: dashboard, brand page, stories, products, analytics |
| Member 4 | Frontend | Buyer & admin Vue.js pages: homepage, story viewer, orders, admin panel |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue.js 3 (Vite) |
| Backend | Python Flask |
| Database | PostgreSQL |
| ORM | SQLAlchemy + Flask-Migrate |
| Testing | Pytest |
| Version Control | GitHub |
| Project Management | Jira |

---

## Repository Structure

```
SoftwareEngineering/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── config.py            # Config (dev/prod settings)
│   │   ├── models/              # SQLAlchemy models — one file per table group
│   │   │   └── __init__.py
│   │   ├── routes/              # Flask blueprints — one file per role/feature
│   │   │   └── __init__.py
│   │   └── utils/               # Shared helper functions
│   │       └── __init__.py
│   ├── migrations/              # Flask-Migrate migrations (auto-generated, commit these)
│   ├── tests/                   # Pytest test files
│   │   └── __init__.py
│   ├── requirements.txt         # All Python dependencies
│   ├── run.py                   # Entry point — runs the Flask dev server
│   └── .env                     # Secret keys & DB URL — DO NOT COMMIT (see .gitignore)
│
├── frontend/
│   ├── src/
│   │   ├── assets/              # Images, fonts, global CSS
│   │   ├── components/          # Reusable Vue components (Navbar, Modal, etc.)
│   │   ├── views/               # Full pages — one .vue file per route
│   │   │   ├── auth/            # Login, Signup, Verify pages
│   │   │   ├── artist/          # All artist-facing pages
│   │   │   ├── buyer/           # All buyer-facing pages
│   │   │   └── admin/           # All admin pages
│   │   ├── router/
│   │   │   └── index.js         # Vue Router — all route definitions live here
│   │   ├── stores/              # Pinia stores for global state
│   │   │   └── auth.js          # Auth state: current user, role, token
│   │   ├── App.vue              # Root Vue component
│   │   └── main.js              # Vue app entry point
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md                    # This file
```

**Key conventions:**
- `views/` holds full pages. `components/` holds reusable pieces shared across pages.
- Backend routes use Flask **Blueprints** — one blueprint per role: `routes/artist.py`, `routes/buyer.py`, `routes/admin.py`, `routes/auth.py`.
- Never hardcode secrets. Always use `.env` and load via `python-dotenv`.

---

## Getting Started

### Prerequisites

Make sure you have the following installed:
- Python 3.10+
- Node.js 18+ and npm
- PostgreSQL 14+
- Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/SoftwareEngineering.git
cd SoftwareEngineering
```

---

### 2. Backend Setup

This section walks through setting up the Flask backend from scratch on a new machine. Follow every step in order.

#### Step 1 — Navigate to the backend directory

```bash
cd backend
```

---

#### Step 2 — Create and activate a Python virtual environment

A virtual environment keeps project dependencies isolated from your system Python.

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should now see `(venv)` at the start of your terminal prompt. Every subsequent Python/pip/flask command must be run with the venv active. If you open a new terminal, re-run the activate command above before continuing.

---

#### Step 3 — Install Python dependencies

```bash
pip install -r requirements.txt
```

This installs Flask, SQLAlchemy, Flask-Migrate, psycopg2 (PostgreSQL driver), JWT, and all other dependencies listed in `requirements.txt`.

---

#### Step 4 — Set up PostgreSQL

##### 4a. Access the PostgreSQL shell

On Linux, the default PostgreSQL installation uses **peer authentication**, which means you must switch to the `postgres` system user to access the shell. Running `psql -U postgres` directly from your own user will fail with a `Peer authentication failed` error.

The correct way to open the PostgreSQL shell is:

```bash
sudo -i -u postgres
psql
```

This switches your terminal session to the `postgres` system user and opens the interactive psql prompt. You should see `postgres=#`.

##### 4b. Create the database and application user

Run the following SQL commands inside the psql shell:

```sql
CREATE DATABASE kala_db;
CREATE USER kala_user WITH PASSWORD 'kala_pass';
GRANT ALL PRIVILEGES ON DATABASE kala_db TO kala_user;
\q
```

- `\q` exits the psql shell.
- After `\q`, run `exit` to return to your normal user session.

```bash
exit
```

> **Note:** The password `kala_pass` is the shared development password used by the whole team. Never use this in production.

##### 4c. Verify the connection (optional but recommended)

To confirm the new user and database work correctly, run:

```bash
psql -U kala_user -d kala_db -h localhost
```

If it opens the psql prompt (`kala_db=>`), your database is set up correctly. Type `\q` to exit.

> If this still fails with a peer authentication error, use `-h localhost` as shown — this forces TCP connection instead of Unix socket, which bypasses peer auth.

---

#### Step 5 — Create your `.env` file

The `.env` file stores secrets and environment-specific config. It is **never committed to git**.

Copy the example template:

```bash
cp .env.example .env
```

Open `.env` in your editor and fill in the values:

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=some-hard-to-guess-string-change-this
DATABASE_URL=postgresql://kala_user:kala_pass@localhost:5432/kala_db
```

- `SECRET_KEY` can be any long random string during development.
- `DATABASE_URL` uses the user, password, and database name you created in Step 4.

---

#### Step 6 — Initialise Flask-Migrate

Flask-Migrate manages database schema changes using Alembic. Run `flask db init` **only once per project clone** — it creates the `migrations/` tracking folder.

```bash
flask db init
```

> If the `migrations/` folder is already present in the repo (it will be once a teammate commits it), **skip this step**. Running it again will overwrite migration history.

---

#### Step 7 — Verify the database connection

Before running any migrations, confirm Flask can actually reach the database:

```bash
flask shell
```

Inside the shell, run:

```python
from app import db
db.engine.connect()
exit()
```

If no error is thrown, the connection is working. If you see an `OperationalError`, double-check your `DATABASE_URL` in `.env` and confirm PostgreSQL is running (`sudo systemctl status postgresql`).

---

#### Step 8 — Run the Flask development server

```bash
flask run
```

The backend will be available at `http://localhost:5000`.

To verify it is running, open a browser or use curl:

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{"status": "ok"}
```

---

#### Step 9 — (When models are defined) Run migrations

Once SQLAlchemy models have been added to `app/models/`, you will need to generate and apply a migration to create the corresponding tables in the database. This step is **not needed yet** — it will be done as part of Task 3.

```bash
flask db migrate -m "describe what changed"
flask db upgrade
```

- `flask db migrate` auto-generates a migration script by comparing your models to the current database state.
- `flask db upgrade` applies pending migrations to the database.
- Always commit the generated file in `migrations/versions/` to git so your teammates can run `flask db upgrade` to sync their local database.

---

### 3. Frontend Setup

```bash
cd ../frontend
```

**Install dependencies:**
```bash
npm install
```

**Run the Vue development server:**
```bash
npm run dev
```
The frontend will be available at `http://localhost:5173`.

> During development the frontend and backend run on separate ports. Vue's dev server proxies API requests to Flask — this is configured in `vite.config.js`.

---

## Common Issues & Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| `Peer authentication failed for user "postgres"` | psql uses Unix socket auth by default | Use `sudo -i -u postgres` then `psql`, or connect via TCP with `-h localhost` |
| `FATAL: database "kala_db" does not exist` | DB not created yet | Follow Step 4b above |
| `ModuleNotFoundError` when running Flask | venv not activated | Run `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows) |
| `flask: command not found` | venv not activated | Same as above |
| `connection refused` on port 5432 | PostgreSQL not running | Run `sudo systemctl start postgresql` |
| `.env` not found / empty DATABASE_URL | `.env` not created | Run `cp .env.example .env` and fill in values |

---

## Branching Strategy

We follow a simple feature-branch workflow:

```
main          ← stable, production-ready code only
dev           ← integration branch, merge features here first
feature/xyz   ← individual feature branches, branched from dev
```

**Rules:**
- Never commit directly to `main`.
- All changes go through a Pull Request with at least one reviewer.
- Branch names should be descriptive: `feature/artist-login`, `feature/story-editor`, `fix/order-status-bug`.

---

## Milestones & Deadlines

| Milestone | Focus | Deadline |
|-----------|-------|----------|
| Milestone 1 | Problem Statement & User Identification | Feb 22, 2026 ✅ |
| Milestone 2 | Scheduling, Design & Frontend | Mar 22, 2026 |
| Sprint 1 | Core Artist APIs & Testing | Apr 5, 2026 |
| Sprint 2 | Buyer, Admin & AI APIs | Apr 14, 2026 |
| Milestone 5 | Final Submission & Presentation | Apr 20, 2026 |

---

## User Roles

| Role | Description |
|------|-------------|
| **Artist** | Independent seller. Creates a brand profile, manages products, publishes Stories, views analytics and orders. Must be verified by Admin before receiving orders. |
| **Buyer** | Browses artist brand pages and Stories, places orders, leaves reviews, follows artists. |
| **Admin** | Manages the platform. Approves/rejects artist verifications, manages users, views platform-wide analytics. |

---

## Environment Variables Reference

| Variable | Description |
|----------|-------------|
| `FLASK_APP` | Entry point for Flask (`run.py`) |
| `FLASK_ENV` | `development` or `production` |
| `SECRET_KEY` | Flask session secret key |
| `DATABASE_URL` | PostgreSQL connection string |

> A `.env.example` file with empty values is committed to the repo as a template. The actual `.env` file is in `.gitignore` and must never be committed.

---

## .gitignore

The following are excluded from version control:

```
# Python
backend/.env
backend/venv/
backend/__pycache__/
backend/**/*.pyc
backend/instance/

# Node
frontend/node_modules/
frontend/dist/

# OS
.DS_Store
Thumbs.db
```

---

*This README will be updated as the project evolves across milestones and sprints.*