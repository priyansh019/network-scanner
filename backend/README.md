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