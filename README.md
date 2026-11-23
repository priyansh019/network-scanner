# SentinelPy — Network Security Scanner

SentinelPy is a full-stack network security scanning tool for discovering open ports, identifying services, and collecting basic vulnerability and risk information.

> Only scan systems you own or have explicit permission to test.

## Features

- Concurrent TCP port scanning
- Service banner and version detection
- Local CVE matching and risk classification
- JWT authentication
- Scan history and result dashboard
- React frontend and FastAPI backend
- SQLite development and PostgreSQL deployment support

## Tech Stack

- **Frontend:** React, Vite
- **Backend:** FastAPI, SQLAlchemy, Alembic
- **Scanner:** Python
- **Database:** SQLite or PostgreSQL

## Setup

### Backend

```bash
cd backend
cp .envexample .env
uv sync
alembic upgrade head
uvicorn app.main:app --reload
```

API: `http://127.0.0.1:8000`  
Swagger: `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard: `http://127.0.0.1:5173`

### Scanner

```bash
cd scanner
pip install -r requirements.txt
python advanced_scanner.py
```

To poll and execute queued backend scans:

```bash
python poller.py
```

Configure the scanner through `.env`:

```env
BACKEND_URL=http://127.0.0.1:8000
SCANNER_EMAIL=scanner@example.com
SCANNER_PASSWORD=change-me
```

## API

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/api/v1/auth/register` | Register |
| `POST` | `/api/v1/auth/login` | Authenticate |
| `POST` | `/api/v1/scan/start` | Start a scan |
| `GET` | `/api/v1/scan/history` | View history |
| `GET` | `/api/v1/scan/{id}` | View a scan |

## License

No license is currently specified.
