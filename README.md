# SentinelPy — Network Security Scanner

SentinelPy is a full-stack network security scanning platform. It lets a user request a scan of a target IP/hostname, runs a concurrent port scanner that fingerprints services and matches them against a vulnerability database, and displays the results — open ports, detected services, and risk level — on a web dashboard.

The project is split into three parts that work together:

| Part | What it does |
|------|---------------|
| **Frontend** | React (Vite) dashboard for logging in, starting scans, and viewing scan history/results |
| **Backend** | FastAPI REST API that handles auth, stores scan requests, and receives results |
| **Scanner** | Python scanning engine that performs the actual port scan, service fingerprinting, and CVE/risk matching, then reports back to the backend |

**Live app:**
- Live at : https://network-scanner-2-umx2.onrender.com
- Backend API: `https://network-scanner-1-p3wn.onrender.com`
- API Docs (Swagger): `https://network-scanner-1-p3wn.onrender.com/docs`

---

## How it fits together

```
┌────────────┐        REST/JWT        ┌────────────┐        REST/JWT        ┌────────────┐
│  Frontend  │  ───────────────────▶  │  Backend    │  ◀───────────────────  │  Scanner    │
│  (React)   │  ◀───────────────────  │  (FastAPI)  │  ───────────────────▶  │  (Python)   │
└────────────┘   scan requests /      └────────────┘   polls for new scans,  └────────────┘
                  scan history                          submits results
```

1. A user registers/logs in and starts a scan from the **frontend**.
2. The **backend** creates a scan record (status: `initiated`) and exposes it via the API.
3. The **scanner** (running as a separate process/poller) authenticates with the backend, picks up pending scans, scans the target's ports, fingerprints services, checks them against a vulnerability database, and calculates a risk level.
4. The scanner posts the results back to the backend, which updates the scan record.
5. The **frontend** polls/fetches the scan history and results and renders them on the dashboard.

---

## Project Structure

```
network-scanner/
├── frontend/            # React + Vite dashboard
│   ├── src/
│   │   ├── pages/         # Login, Register, Dashboard, StartScan, ScanHistory, ScanResult
│   │   ├── components/    # Navbar, RiskBadge, etc.
│   │   └── api.js         # Axios client for backend API
│   └── package.json
│
├── backend/              # FastAPI REST API
│   ├── app/
│   │   ├── main.py            # App entry point, middleware, CORS
│   │   ├── config.py          # Environment/config loading
│   │   ├── database.py        # SQLAlchemy engine/session
│   │   ├── core/               # Security (JWT) and auth dependencies
│   │   ├── api/routes/         # auth.py, scan.py, mock_scanner.py
│   │   └── model/              # Pydantic + SQLAlchemy models
│   ├── migrations/         # Alembic migrations
│   ├── render.yaml          # Render deployment config
│   └── requirements.txt
│
├── scanner/               # Scanning engine
│   ├── scanner.py             # Basic standalone port scanner
│   ├── advanced_scanner.py    # CLI entry point for a full scan + backend report
│   ├── integration.py         # Auth, scanning, fingerprinting, backend reporting
│   ├── poller.py               # Polls backend for new scans and runs them automatically
│   ├── modules/
│   │   ├── version_detector.py   # Extracts service/version from banners
│   │   ├── cve_matcher.py        # Matches service+version to known vulnerabilities
│   │   └── risk_classifier.py    # Converts severity to a risk label
│   └── databases/vulnerabilities.json  # Local vulnerability lookup table
│
├── Roadmap/                # Project planning docs (roadmap, roles, timeline)
└── .envexample
```

---

## Tech Stack

- **Frontend:** React 18, React Router, Axios, Vite
- **Backend:** FastAPI, SQLAlchemy, Alembic, Pydantic, JWT auth, SQLite (dev), Gunicorn/Uvicorn
- **Scanner:** Python sockets, `ThreadPoolExecutor` for concurrent port scanning, `requests` for backend integration
- **Deployment:** Render (backend), configured via `render.yaml`

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- `uv` (or `pip`) for Python dependency management

### 1. Clone the repo

```bash
git clone https://github.com/priyansh019/network-scanner.git
cd network-scanner
cp .envexample .env
```

### 2. Backend

```bash
cd backend
uv sync                     # or: pip install -r requirements.txt
alembic upgrade head        # run database migrations
uvicorn app.main:app --reload
```

Backend runs at `http://127.0.0.1:8000` — interactive docs at `http://127.0.0.1:8000/docs`.

See [`backend/README.md`](backend/README.md) for the full API reference and endpoint details.

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://127.0.0.1:5173`.

### 4. Scanner

The scanner authenticates against the backend as its own "scanner account," so it needs credentials in its `.env`:

```bash
cd scanner
pip install -r requirements.txt
```

```
BACKEND_URL=http://127.0.0.1:8000
SCANNER_EMAIL=scanner@example.com
SCANNER_PASSWORD=change-me
```

Run it in one of two modes:

- **On-demand:** `python advanced_scanner.py` — manually enter a `scan_id`, target, and ports.
- **Automatic poller:** `python poller.py` — continuously polls the backend for scans with status `initiated` and runs them automatically.

---

## Core API Endpoints (Backend)

| Method | Endpoint | Description |
|--------|----------|--------------|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Log in and receive a JWT |
| GET | `/api/v1/scan/status` | Check scanner/service status |
| POST | `/api/v1/scan/start` | Initiate a new scan |
| GET | `/api/v1/scan/history` | List scan history |
| GET | `/api/v1/scan/{id}` | Get a single scan by ID |
| PATCH | `/api/v1/scan/{id}/status` | Update scan status |
| POST | `/api/v1/scan/{id}/results` | Submit scan results (used by the scanner) |

Full request/response examples are in [`backend/README.md`](backend/README.md).

---

## What the Scanner Does

For each target port, the scanner:
1. Attempts a TCP connection to check if the port is open.
2. Grabs a service banner and fingerprints the service (Apache, Nginx, OpenSSH, MySQL, PostgreSQL, etc.), falling back to a port-based guess if no banner is available.
3. Extracts a version number from the banner where possible.
4. Looks up the service + version in the local vulnerability database to flag known CVEs.
5. Classifies the resulting risk (`low`, `medium`, `high`, `critical`) per port, then rolls this up into an overall risk level for the scan.
6. Authenticates with the backend (JWT, auto-refreshed on expiry) and posts the results.

---

## Deployment

The backend is deployed on **Render** using [`backend/render.yaml`](backend/render.yaml):
- Build: `pip install uv && uv sync`
- Start: runs Alembic migrations, then serves the app with Gunicorn + Uvicorn workers
- Environment variables (`DATABASE_URL`, `APP_TITLE`, `DEBUG`, `SECRET_KEY`, `ALLOWED_ORIGINS`) are configured in the Render dashboard / `render.yaml`

---

## Team & Roles

This project was built collaboratively:
- **Backend, Frontend & Integration:** built and wired together by Preet kasana -- the FastAPI backend, the React frontend, and the scanner-to-backend integration, plus deployment to Render.
- **Scanner Engine:** built by  Priyansh singh — the core port scanning, service fingerprinting, and CVE/risk-matching logic in `scanner/`.

See the [`Roadmap/`](Roadmap) folder for the original project roadmap, role division, and timeline documents.

---

## Git Workflow

- Never commit directly to `main`
- Feature work happens on dedicated branches (e.g. `backend-fastapi-setup`)
- Open a PR for review before merging
