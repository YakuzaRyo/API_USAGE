## ADDED Requirements

### Requirement: Start scheduler on application startup

The system SHALL initialize an APScheduler AsyncIOScheduler during FastAPI lifespan startup, register collection jobs for all providers with `interval_seconds > 0`, and shut down the scheduler on application stop.

#### Scenario: Scheduler starts with existing providers

- **WHEN** the application starts and there are providers with interval_seconds > 0
- **THEN** each such provider has a scheduled job registered with its configured interval

#### Scenario: Providers with manual mode are skipped

- **WHEN** the application starts and a provider has interval_seconds = 0
- **THEN** no scheduled job is created for that provider

### Requirement: Register new job on provider creation

The system SHALL register a new scheduled job when a provider is created with `interval_seconds > 0`.

#### Scenario: Auto-collect enabled on creation

- **WHEN** a provider is created with interval_seconds = 300
- **THEN** a job is registered to collect usage for that provider every 300 seconds

### Requirement: Update job on provider interval change

The system SHALL remove the existing job and register a new one when a provider's `interval_seconds` is updated.

#### Scenario: Interval changed

- **WHEN** a provider's interval_seconds is changed from 300 to 60
- **THEN** the old 300s job is removed and a new 60s job is registered

#### Scenario: Switched to manual mode

- **WHEN** a provider's interval_seconds is changed from 300 to 0
- **THEN** the scheduled job is removed and no new job is registered

### Requirement: Remove job on provider deletion

The system SHALL remove the scheduled job when a provider is deleted.

#### Scenario: Provider deleted

- **WHEN** a provider with an active scheduled job is deleted
- **THEN** the job is removed from the scheduler

### Requirement: Minimum interval enforcement

The system SHALL enforce a minimum interval of 10 seconds. Any `interval_seconds` value between 1 and 9 SHALL be rejected with a validation error.

#### Scenario: Interval too small

- **WHEN** a provider is created or updated with interval_seconds = 5
- **THEN** returns 422 with error "interval_seconds must be 0 (manual) or >= 10"
