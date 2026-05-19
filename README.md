# RILL

RILL is a real estate market researcher for Hyderabad-area investment discovery.

This MVP analyzes localities within roughly 50 km of Hyderabad using:

- FastAPI backend
- Next.js frontend
- PostgreSQL persistence
- Pluggable trend collectors
- Transparent investment scoring

The current collector ships with seed market signals so the app is usable without fragile scraping. The backend also includes an HTML table collector for approved/public pages that expose trend data in simple tables.

## Run Locally

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DATABASE_URL="sqlite:///./rill.db"
uvicorn app.main:app --reload --port 8000
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## PostgreSQL

For the full stack with PostgreSQL, use Docker Compose from the repo root:

```powershell
docker compose up --build
```

Frontend: `http://localhost:3000`

Backend docs: `http://localhost:8000/docs`

If Docker was just installed, open a new PowerShell window and make sure Docker Desktop is running before using `docker compose`.

## MVP Features

- ranks Hyderabad-area localities within a 50 km radius
- filters by acquisition budget
- supports balanced, rental income, appreciation, and lower-risk strategies
- calculates estimated gross rental yield
- explains the investment thesis and risk flags
- exposes `/api/refresh` for collecting/upserting market signals
- includes an approved HTML table collector for source pages you are allowed to scrape

## Data Strategy

The app intentionally avoids scraping restricted listing pages by default. Recommended production sources:

- Telangana open data and municipal permits
- HMDA/GHMC development notices where available
- RERA project data
- approved real estate APIs
- source-specific scrapers only where terms permit automated access
