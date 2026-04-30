# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

LLM Usage Monitor — a full-stack web app that tracks LLM API usage (tokens, cost, balance) across multiple providers. The backend periodically polls each provider's usage/balance APIs, stores snapshots, and exposes stats endpoints. The frontend renders dashboards with ECharts.

## Dev commands

```bash
# Backend (from backend/)
cd backend && uv run uvicorn main:app --reload --port 8000

# Frontend (from frontend/)
cd frontend && npm run dev          # Vite dev server on :5173, proxies /api → :8000
cd frontend && npm run build        # Type-check + production build
cd frontend && npm run preview      # Preview production build
```

- Python dependencies managed by `uv` (`pyproject.toml`, `uv.lock`). The venv is at `backend/.venv/`.
- Frontend dependencies via npm.
- Alembic migrations run automatically on backend startup (in `lifespan`). There is no manual migrate command.

## Architecture

```
frontend (Vue 3 + TS + Pinia + ECharts, :5173)
  └─ proxies /api → backend (FastAPI + SQLAlchemy async + SQLite, :8000)
```

### Backend layers

| Layer | Files | Role |
|---|---|---|
| Entrypoint | `main.py` | FastAPI app, lifespan (migrations → init DB → scheduler), CORS, router registration |
| Config | `config.py` | Pydantic-settings: `DATABASE_URL`, `SECRET_KEY`, `CORS_ORIGINS` (from `.env`) |
| DB | `database.py` | Async engine (aiosqlite), WAL pragma, session factory, `init_db()` / `get_db()` |
| Models | `models.py` | `Provider` → `UsageRecord` + `CollectionLog` (ORM relationships) |
| Routers | `routers/providers.py`, `routers/stats.py` | REST endpoints under `/api/` |
| Services | `services/collector.py`, `scheduler.py`, `crypto.py` | Core business logic |
| Logging | `logging_config.py` | JSON file logs (daily + size rotation) + console output |
| Migrations | `alembic/` | Auto-run on startup; migration engine uses a **sync** SQLite connection |

### Three database models

- **Provider** — API credentials (Fernet-encrypted `api_key`), polling config (`interval_seconds`), billing mode (`api` or `token_plan`), JSON column `usage_mapping`/`balance_mapping` that maps API response paths (dot-notation) to fields. Soft-delete via `deleted` flag.
- **UsageRecord** — per-model token/cost snapshot, written each collection cycle.
- **CollectionLog** — audit log of every collection attempt (status, record count, balance, error message).

### Two billing modes

- `api` (default): consumed amount = sum of balance decreases between consecutive `CollectionLog` snapshots (top-ups are skipped by ignoring positive diffs).
- `token_plan`: `monthly_fee × months_since(sub_start_date)`.

### Scheduler

`APScheduler` (AsyncIOScheduler) runs in-process. On startup, all providers with `interval_seconds > 0` get a recurring job that calls `collect_usage()`. Jobs are dynamically added/removed/rescheduled on provider CRUD. Minimum interval is 10 seconds.

### Collector (`services/collector.py`)

Calls provider's usage API → extracts `total_tokens` and `cost` via `.`-notation path mappings → writes one `UsageRecord` per model (splits evenly). Then optionally calls the balance API → updates `provider.last_balance` and logs the balance snapshot. Each outcome creates a `CollectionLog`.

### Crypto (`services/crypto.py`)

API keys are Fernet-encrypted at rest. Key stored in `data/.fernet_key` (auto-generated) or from `SECRET_KEY` env var. Keys are masked (`...xxxx`) when returned to the frontend. The raw key is never sent to clients.

### Frontend structure

- Two routes defined in `src/router/index.ts`: `/dashboard` (DashboardView) and `/providers` (ProviderView). `/` redirects to `/dashboard`.
- Two Pinia stores: `useProvidersStore` (CRUD + trigger collection) and `useUsageStore` (summary, trends, distribution, balance history, billing summary — auto-refetches when `selectedProviderId` changes via `watch`).
- `src/api/index.ts` — all Axios calls and TypeScript interfaces.
- `App.vue` — sidebar layout with nav links.
- Chart views use ECharts 6 (`echarts` npm package).

### API design pattern

All stats endpoints accept an optional `provider_id` query parameter. When absent, they aggregate across all non-deleted providers. When present, they filter to that provider and return its name/currency_symbol in the response.

## Important constraints

- SQLite with WAL mode. Async via `aiosqlite` + SQLAlchemy async. **Alembic migrations require a sync engine** — `main.py` creates a temporary sync engine just for migration, then disposes it.
- `Provider.api_key` is stored encrypted. Always decrypt before use (`decrypt(provider.api_key)`), mask before returning to clients (`mask_key()`).
- Soft-delete: set `provider.deleted = True`, never hard-delete rows (preserves foreign keys in `UsageRecord` and `CollectionLog`).
- Datetime fields use `.astimezone()` (local timezone-aware). The `now_local()` helper in `models.py` sets defaults.
- The frontend dev server proxies `/api` to `http://localhost:8000` — CORS on the backend allows `http://localhost:5173`.
