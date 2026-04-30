# LLM Usage Monitor

A full-stack web application that tracks LLM API usage (tokens, cost, balance) across multiple providers. The backend periodically polls each provider's usage/balance APIs, stores snapshots, and exposes stats endpoints. The frontend renders dashboards with ECharts.

## Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | Vue 3, TypeScript, Pinia, ECharts 6, Axios, Lucide Icons |
| Backend | FastAPI, SQLAlchemy (async), SQLite (WAL mode), APScheduler |
| Build | Vite, uv |

## Prerequisites

- Python >= 3.12
- Node.js >= 18
- [uv](https://docs.astral.sh/uv/) (Python package manager)

## Quick Start

### 1. Backend

```bash
cd backend
uv sync                # install dependencies
cp ../.env.example .env  # configure if needed
uv run uvicorn main:app --reload --port 8000
```

The backend runs at `http://localhost:8000`. Alembic migrations run automatically on startup.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev            # dev server on :5173, proxies /api → :8000
```

Open `http://localhost:5173` in your browser.

## Project Structure

```
frontend/                    # Vue 3 + TypeScript frontend
  src/
    api/                     # Axios calls & TypeScript interfaces
    components/              # Reusable UI components
    router/                  # Vue Router (/dashboard, /providers)
    stores/                  # Pinia stores (providers, usage)
    views/                   # Page-level views
  vite.config.ts             # Dev server with /api proxy
backend/                     # FastAPI backend
  routers/                   # REST endpoints (providers, stats, categories)
  services/                  # Business logic (collector, scheduler, crypto)
  alembic/                   # Database migrations (auto-run on startup)
  data/                      # SQLite database & Fernet key (gitignored)
  config.py                  # Settings from .env
  database.py                # Async engine & session factory
  main.py                    # FastAPI app & lifespan
  models.py                  # SQLAlchemy ORM models
```

## Configuration

Create a `.env` file in the `backend/` directory (or project root):

```env
DATABASE_URL=sqlite+aiosqlite:///./data/app.db
SECRET_KEY=                 # optional; auto-generates if empty
CORS_ORIGINS=["http://localhost:5173"]
```

A Fernet encryption key is auto-generated at `data/.fernet_key` on first run to encrypt stored API keys.

## Features

- **Multi-provider support** — Add multiple LLM providers with their API keys and endpoints
- **Automatic polling** — Configurable interval per provider, minimum 10 seconds
- **Two billing modes** — `api` (balance diff tracking) and `token_plan` (monthly subscription)
- **Encrypted API keys** — Fernet encryption at rest; keys are masked in API responses
- **Dashboard charts** — Usage trends, cost distribution, balance history (ECharts)
- **Category management** — Group providers by category
- **Soft delete** — Providers are soft-deleted to preserve historical data
- **Audit logging** — Every collection attempt is logged with status and details

## API Overview

All stats endpoints accept an optional `provider_id` query parameter for filtering.

| Endpoint | Description |
|---|---|
| `GET /api/providers` | List all providers |
| `POST /api/providers` | Create a provider |
| `PUT /api/providers/{id}` | Update a provider |
| `DELETE /api/providers/{id}` | Soft-delete a provider |
| `POST /api/providers/{id}/collect` | Trigger manual collection |
| `GET /api/stats/summary` | Usage summary (tokens, cost) |
| `GET /api/stats/trends` | Usage trends over time |
| `GET /api/stats/distribution` | Token/cost distribution by model |
| `GET /api/stats/balance-history` | Balance history chart data |
| `GET /api/stats/billing-summary` | Billing summary |
| `GET /api/categories` | List categories |
| `POST /api/categories` | Create a category |

## Build for Production

```bash
cd frontend && npm run build     # outputs to frontend/dist/
cd backend && uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

Serve `frontend/dist/` with any static file server and ensure it proxies `/api` to the backend.

## License

Private project.
