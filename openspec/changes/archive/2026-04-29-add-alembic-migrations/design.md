## Context

- SQLite database with async SQLAlchemy (`aiosqlite`)
- 3 tables: `providers`, `usage_records`, `collection_logs`
- Current drift: `collection_logs.balance` exists in model but NOT in DB
- No existing migration infrastructure
- Fernet keys stored in file system (`data/.fernet_key`), not in DB

## Goals / Non-Goals

**Goals:**
- Fix the `collection_logs.balance` column drift
- Enable future schema changes via `alembic revision --autogenerate`
- Auto-run migrations on application startup
- Zero-downtime for existing databases (first migration is additive only)

**Non-Goals:**
- Downgrade support (SQLite has limited ALTER support, downgrades are rarely useful for this project)
- Data migration (only schema migration for now)
- Docker-based migration execution

## Decisions

### Decision 1: Alembic with async engine

Use Alembic's async template (`alembic init -t async`) to match the existing `AsyncEngine` / `aiosqlite` stack.

**Why not sync Alembic?** The project already uses async SQLAlchemy throughout. Mixing sync and async engines in the same app creates dual-engine management overhead.

**Why not a manual SQL approach?** Manual `ALTER TABLE` in `init_db` works once but doesn't scale. Each new column requires a developer to remember to write the ALTER manually. Alembic's `--autogenerate` compares model metadata to the live database and generates the diff automatically.

### Decision 2: Baseline + add-missing-column

```
migrations/
├── env.py          (Alembic async config)
├── script.py.mako  (migration template)
├── alembic.ini     (Alembic config)
└── versions/
    ├── 001_baseline.py          (current full schema as create_all)
    └── 002_add_balance_column.py (ALTER TABLE collection_logs ADD balance FLOAT)
```

The baseline captures the schema exactly as `Base.metadata.create_all` would produce it (all 3 tables, all columns including `balance`). For existing databases: `001_baseline` is skipped since tables exist; `002` adds the missing column. For fresh databases: `001` creates everything, `002` is a no-op.

**Why not a single migration?** Two migrations clearly separate "this is the intended schema" from "this is the fix for existing databases." The second migration can be marked as already-applied on fresh installs since `create_all` already includes the column.

### Decision 3: Startup integration

In `main.py` lifespan, before scheduler init:

```python
from alembic.config import Config
from alembic import command

alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "head")
```

This runs synchronously (blocking) at startup since migrations must complete before any queries. For a single-user SQLite app, this is acceptable.

### Decision 4: Keep `create_all` as fresh-install optimization

For a fresh database (no tables exist), `create_all` + stamping the baseline revision as applied is faster than running the baseline migration. The startup logic:

```python
async with engine.connect() as conn:
    tables = await conn.run_sync(lambda sync_conn: ...)
    if no_tables:
        await conn.run_sync(Base.metadata.create_all)
        # Stamp baseline as applied without running it
        command.stamp(alembic_cfg, "001_baseline")
    # Then run remaining migrations
    command.upgrade(alembic_cfg, "head")
```

## Risks / Trade-offs

- **[Risk] alembic.ini contains hardcoded DB URL** → Mitigation: Use `alembic/env.py` to read from `config.Settings` instead of `alembic.ini`
- **[Risk] Fresh DB creates `balance` column in `create_all`, then `002` tries to add it again** → Mitigation: `002` uses `op.add_column` with error handling, or we stamp `002` as applied too. Actually, since `create_all` includes it, both revisions should be stamped. Better: use only `upgrade head` and drop `create_all` entirely.
- **[Trade-off] Async Alembic has less community support than sync** → Acceptable: this is a single-developer tool; migrations are run once at startup under controlled conditions.
