# SentinelPy Backend

> FastAPI backend for the SentinelPy network security scanning platform.

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