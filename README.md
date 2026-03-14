# __Kala__ — Multi-Vendor Catalogue Marketplace Platform

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

```bash
cd backend
```

**Create and activate a virtual environment:**

On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Create your `.env` file:**
```bash
cp .env.example .env
```
Then open `.env` and fill in your values:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/artistry_db
```

**Set up the database:**
```bash
flask db init        # only needed the first time
flask db migrate -m "initial migration"
flask db upgrade
```

**Run the Flask development server:**
```bash
flask run
```
The backend will be available at `http://localhost:5000`.

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
