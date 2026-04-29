## Why

The project uses SQLAlchemy's `Base.metadata.create_all()` for database initialization, which only creates tables that don't exist — it cannot alter existing tables. The `collection_logs` table is already missing its `balance` column (present in the model but absent from the actual SQLite database). Any INSERT or SELECT touching this column will crash. Introducing Alembic provides a standard, repeatable way to evolve the schema over time, fix the current drift, and prevent future mismatches.

## What Changes

- Add `alembic` as a dependency and run `alembic init` to scaffold the migration directory
- Configure Alembic to use the project's async SQLAlchemy engine and model metadata
- Generate a baseline migration that captures the current schema as it should be (with `collection_logs.balance`)
- Integrate `alembic upgrade head` into application startup so migrations run automatically
- Replace manual `create_all` with migrations as the canonical schema management strategy

## Capabilities

### New Capabilities

- `db-migrations`: Standard Alembic-based database migration system with auto-generation and automatic startup migration for async SQLite

### Modified Capabilities

None — existing features work the same; only the schema management layer changes.

## Impact

- **Backend dependencies**: Add `alembic` to `requirements.txt` or `pyproject.toml`
- **Backend files**: `database.py` (add migration runner, keep `create_all` as fallback), `config.py` (add migration-related settings), new `migrations/` directory
- **Startup**: `main.py` lifespan calls migration before scheduler init
- **No API changes**, no frontend changes
