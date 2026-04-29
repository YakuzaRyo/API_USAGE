# Database Migrations

## Purpose

Standard Alembic-based migration system for the async SQLite database, replacing `Base.metadata.create_all` as the canonical schema management strategy. Provides auto-generation, version history, and automatic startup migration.

## ADDED Requirements

### Requirement: Alembic migration scaffold
The project SHALL include an Alembic migration environment configured for async SQLAlchemy with the project's model metadata.

#### Scenario: Migration directory structure exists
- **WHEN** the project is set up
- **THEN** an `alembic.ini` and `migrations/` directory with `env.py`, `script.py.mako`, and `versions/` subdirectory exist in the backend

#### Scenario: Alembic reads DB URL from app config
- **WHEN** `env.py` needs a database URL
- **THEN** it reads from `config.Settings` rather than hardcoding in `alembic.ini`

### Requirement: Baseline migration
A baseline migration SHALL capture the full current schema as `Base.metadata.create_all` would produce it, including all three tables (`providers`, `usage_records`, `collection_logs`) with all columns.

#### Scenario: Baseline migration idempotent
- **WHEN** the baseline migration is run against a fresh database
- **THEN** all tables and columns are created matching the model definitions

### Requirement: Missing column migration
A migration SHALL add the missing `balance` column (Float, nullable) to the `collection_logs` table for databases created before this column was added to the model.

#### Scenario: Balance column added to existing database
- **WHEN** an existing database without `collection_logs.balance` is migrated
- **THEN** a `balance` column (FLOAT, nullable) is added to `collection_logs`

#### Scenario: Balance column on fresh database
- **WHEN** a fresh database is created and all migrations run
- **THEN** the `balance` column exists in `collection_logs` without duplicate-add errors

### Requirement: Automatic startup migration
The application SHALL run `alembic upgrade head` during lifespan startup, before the scheduler and before any queries execute.

#### Scenario: Migrations run on startup
- **WHEN** the application starts
- **THEN** all pending migrations are applied before the scheduler registers jobs

#### Scenario: No migrations pending
- **WHEN** the application starts and the database is already at the latest revision
- **THEN** startup proceeds immediately with no errors

### Requirement: Autogenerate capability
Developers SHALL be able to run `alembic revision --autogenerate -m "description"` to generate new migrations from model changes.

#### Scenario: Autogenerate detects new column
- **WHEN** `alembic revision --autogenerate` is run after adding a new column to a model
- **THEN** a migration file is generated with `op.add_column` for the new column
