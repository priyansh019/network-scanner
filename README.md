# SentinelPy — Network Security Scanner

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=20232A)](https://react.dev/)

SentinelPy is a full-stack network security scanning platform. It accepts an IP address or hostname, performs concurrent port discovery and service fingerprinting, checks detected services against local vulnerability data, calculates a risk score, and presents the findings through a web dashboard.

> **Responsible use:** Only scan systems you own or have explicit permission to test.

## Features

- Concurrent TCP port scanning
- Service banner and version detection
- Common service identification
- Known-CVE lookup from a local vulnerability database
- Low, medium, high, and critical risk classification
- JWT-based authentication
- Scan creation, history, status, and result views
- Automatic scanner polling for queued scans
- Separate React frontend and FastAPI backend
- SQLite support for local development and PostgreSQL support for deployment

## Architecture

```text
React + Vite Dashboard
          │  REST / JWT
          ▼
FastAPI Backend ───── SQLite / PostgreSQL
          │  pending scans and results
          ▼
Python Scanner ─── service fingerprints / CVE matching
```

1. A user registers or signs in and starts a scan.
2. The backend stores the request and exposes it through the API.
3. The scanner polls for pending work and performs the requested checks.
4. The scanner returns port, service, CVE, and risk information.
5. The dashboard retrieves and renders the updated scan results.

## Project Structure

```text
network-scanner/
├── frontend/                 # React and Vite dashboard
│   ├── src/
│   │   ├── pages/            # Login, register, dashboard, and scan views
│   │   └── components/       # Shared interface components
│   └── package.json
├── backend/                  # FastAPI REST API
│   ├── app/
│   │   ├── api/routes/       # Authentication and scan endpoints
│   │   ├── core/             # Security and application configuration
│   │   └── models/           # Database models
│   ├── migrations/           # Alembic migrations
│   └── requirements.txt
├── scanner/                  # Python scanning engine
│   ├── advanced_scanner.py
│   ├── integration.py
│   ├── poller.py
│   └── modules/
├── databases/                # Local vulnerability lookup data
├── Roadmap/                  # Project planning documents
└── render.yaml               # Render deployment configuration
```

## Technology Stack

| Area | Technologies |
| --- | --- |
| Frontend | React 18, React Router, Axios, Vite |
| Backend | FastAPI, SQLAlchemy, Alembic, Pydantic, JWT |
| Scanner | Python, sockets, ThreadPoolExecutor, requests |
| Database | SQLite for development, PostgreSQL for deployment |
| Deployment | Render, Gunicorn, Uvicorn |

## Prerequisites

- Python 3.11 or newer
- Node.js 18 or newer
- `npm`
- `pip` or `uv`
- Network access to targets you are authorized to scan

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/priyansh019/network-scanner.git
cd network-scanner
cp .envexample .env
```

### 2. Start the backend

```bash
cd backend
uv sync
alembic upgrade head
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive Swagger documentation is available at `http://127.0.0.1:8000/docs`.

Alternatively, install dependencies with pip:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Start the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The dashboard is available at `http://127.0.0.1:5173`.

### 4. Start the scanner

Open a third terminal:

```bash
cd scanner
pip install -r requirements.txt
```

Configure the backend URL and scanner account in `.env`, then choose a mode:

```bash
# Run an interactive scan
python advanced_scanner.py

# Poll the backend and run initiated scans automatically
python poller.py
```

Example environment values:

```env
BACKEND_URL=http://127.0.0.1:8000
SCANNER_EMAIL=scanner@example.com
SCANNER_PASSWORD=change-me
```

## API Overview

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/v1/auth/register` | Register a user |
| `POST` | `/api/v1/auth/login` | Sign in and receive a JWT |
| `GET` | `/api/v1/scan/status` | Check scanner service status |
| `POST` | `/api/v1/scan/start` | Start a new scan |
| `GET` | `/api/v1/scan/history` | List scan history |
| `GET` | `/api/v1/scan/{id}` | Get a scan by ID |
| `PATCH` | `/api/v1/scan/{id}/status` | Update scan status |
| `POST` | `/api/v1/scan/{id}/results` | Submit scanner results |

See the backend README and Swagger UI for request and response details.

## How the Scanner Works

For each target port, the scanner:

1. Opens a TCP connection to determine whether the port is reachable.
2. Reads available service banners and uses a port/service map as a fallback.
3. Extracts a service or version when possible.
4. Matches the detected service and version against the local vulnerability database.
5. Assigns a per-port risk level and an overall risk level for the scan.
6. Authenticates with the backend and submits the collected results.

## Deployment

The backend can be deployed with `backend/render.yaml` and Render environment variables such as:

- `DATABASE_URL`
- `APP_TITLE`
- `DEBUG`
- `SECRET_KEY`
- `ALLOWED_ORIGINS`

The frontend and backend can be deployed separately. Set the frontend API URL to the public backend URL in its deployment environment.

## Contributing

1. Create a focused branch for your change.
2. Keep backend, frontend, and scanner changes separated where practical.
3. Add or update tests and documentation for new behavior.
4. Run formatters and linters before opening a pull request.
5. Never commit real credentials or private target data.

## Team

- **Preet Kasana** — Backend, frontend, integration, and Render deployment
- **Priyansh Singh** — Scanner engine, fingerprinting, and CVE/risk matching

## License

No license is currently specified for this repository.
