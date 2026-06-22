# SentinelPy Backend

> FastAPI backend for the SentinelPy network security scanning platform.

---

## Live API
Base URL: `https://network-scanner-1-p3wn.onrender.com`
API Docs: `https://network-scanner-1-p3wn.onrender.com/docs`

---

## Overview

SentinelPy is a collaborative network security scanning platform. This repository contains the backend API responsible for:

- Accepting and storing scan requests
- Managing scan history
- Receiving scanner engine results
- Exposing clean REST APIs for frontend integration

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| FastAPI | Web framework |
| SQLAlchemy | ORM and database management |
| Alembic | Database migrations |
| SQLite | Database (development) |
| Pydantic | Data validation |
| python-dotenv | Environment variable management |
| uv | Package management |
| uvicorn | ASGI server |

---

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI entry point, middleware, startup
│   ├── config.py         # Environment variable config
│   ├── database.py       # SQLAlchemy engine, session, Base
│   ├── api/
│   │   └── routes/
│   │       └── scan.py   # All scan-related API endpoints
│   └── model/
│       ├── scan.py       # Pydantic request/response models
│       └── db_model.py   # SQLAlchemy database models
├── migrations/           # Alembic migration files
├── .env.example          # Environment variable template
├── alembic.ini           # Alembic configuration
├── pyproject.toml        # Project dependencies
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- fastapi
- uvicorn

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/priyansh019/network-scanner.git
cd network-scanner/backend
```

**2. Install dependencies:**
```bash
uv sync
```

**3. Set up environment variables:**
```bash
cp .env.example .env
```

Edit `.env` with your values:
```
DATABASE_URL=sqlite:///./sentinelpy.db
APP_TITLE=SentinelPy
DEBUG=True
```

**4. Run database migrations:**
```bash
alembic upgrade head
```

**5. Start the development server:**
```bash
uvicorn app.main:app --reload
```

Server runs at `http://127.0.0.1:8000`

Interactive API docs at `http://127.0.0.1:8000/docs`

---

## API Endpoints

### General

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |

### Scan

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/scan/status` | Check scanner status |
| POST | `/api/v1/scan/start` | Initiate a new scan |
| GET | `/api/v1/scan/history` | Get all scan history |
| GET | `/api/v1/scan/{id}` | Get scan by ID |
| PATCH | `/api/v1/scan/{id}/status` | Update scan status |
| POST | `/api/v1/scan/{id}/results` | Submit scanner engine results |

---

## Example Requests

**Start a scan:**
```json
POST /api/v1/scan/start
{
  "target": "192.168.1.1",
  "ports": [22, 80, 443]
}
```

**Submit scan results (scanner engine):**
```json
POST /api/v1/scan/1/results
{
  "scan_id": 1,
  "open_ports": [22, 80],
  "services": {"22": "SSH", "80": "HTTP"},
  "risk_level": "medium"
}
```

**Update scan status:**
```json
PATCH /api/v1/scan/1/status
{
  "status": "completed"
}
```

---

## Team Integration

This backend is designed for integration with:

- **Scanner Engine** — submits results via `POST /api/v1/scan/{id}/results`
- **Frontend Dashboard** — consumes all GET endpoints and displays scan history

CORS is configured for `localhost:3000` and `localhost:5173` in production mode. All origins allowed in DEBUG mode.

---

## Database Migrations

When you change a database model, run:

```bash
alembic revision --autogenerate -m "description of change"
alembic upgrade head
```

To rollback:
```bash
alembic downgrade -1
```

---


---

## Git Workflow

- Never commit directly to `main`
- Backend work lives on `backend-fastapi-setup` branch
- Open a PR for review before merging

---


