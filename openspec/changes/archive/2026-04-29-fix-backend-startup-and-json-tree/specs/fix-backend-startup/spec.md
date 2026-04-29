## ADDED Requirements

### Requirement: Database tables created on startup
The backend SHALL create all required database tables on application startup using SQLAlchemy `Base.metadata.create_all`.

#### Scenario: Fresh database
- **WHEN** the backend starts with no existing database file
- **THEN** all tables (providers, usage_records, collection_logs) are created before any request is served

#### Scenario: Existing database with missing columns
- **WHEN** the backend starts with an existing database file missing new columns
- **THEN** `create_all` runs safely (no-op for existing tables); startup succeeds without errors

### Requirement: No broken Alembic dependency
The backend SHALL NOT reference Alembic configuration files or migration commands that do not exist in the project.

#### Scenario: Startup without alembic.ini
- **WHEN** `alembic.ini` and `alembic/` directory do not exist
- **THEN** the backend starts normally using `init_db()` without errors
