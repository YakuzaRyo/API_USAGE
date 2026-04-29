## 1. Install and scaffold Alembic

- [x] 1.1 Add `alembic` to backend dependencies (requirements.txt or pyproject.toml)
- [x] 1.2 Run `alembic init -t async migrations` in the backend directory
- [x] 1.3 Configure `alembic.ini` — remove hardcoded `sqlalchemy.url`, point `script_location` to `migrations`

## 2. Configure env.py for async SQLAlchemy

- [x] 2.1 Import `Base` from `models`, `settings` from `config`, and async engine from `database`
- [x] 2.2 Set `target_metadata = Base.metadata`
- [x] 2.3 Implement `get_url()` reading from `settings.DATABASE_URL`
- [x] 2.4 Configure `run_migrations_online` to use the async engine and await `upgrade`

## 3. Generate and review baseline migration

- [x] 3.1 Run `alembic revision --autogenerate -m "baseline"` with the current model to capture full schema
- [x] 3.2 Review the generated migration — ensure all 3 tables and all columns (including `collection_logs.balance`) are included
- [x] 3.3 Set `down_revision = None` (first migration)

## 4. Generate balance column migration

- [x] 4.1 Run `alembic revision --autogenerate -m "add balance to collection_logs"` — Alembic should detect the missing column vs existing DB
- [x] 4.2 Verify the migration contains only `op.add_column('collection_logs', sa.Column('balance', sa.Float(), nullable=True))`
- [x] 4.3 Set its `down_revision` to the baseline revision ID

## 5. Integrate with application startup

- [x] 5.1 Add import for `alembic.command` and `alembic.config.Config` in `main.py`
- [x] 5.2 In the lifespan function, before scheduler init, run `command.upgrade(alembic_cfg, "head")`
- [x] 5.3 Remove or comment out `Base.metadata.create_all` from `init_db` usage in lifespan (keep the function for potential tests/manual use)

## 6. Verification

- [x] 6.1 Delete `data/app.db` and start the app — verify all tables are created by migrations
- [x] 6.2 With an existing database (no `balance` column), start the app — verify `balance` column is added and existing data is preserved
- [x] 6.3 Run `alembic revision --autogenerate -m "test"` against the migrated database — verify it generates an empty migration (schema matches models)
- [x] 6.4 Run collector against migrated database — verify `collection_logs.balance` writes succeed
