## ADDED Requirements

### Requirement: Provider CRUD operations are logged
The system SHALL log all create, update, and delete operations on providers with provider_id and operation type.

#### Scenario: Provider created
- **WHEN** a new provider is successfully created via POST /api/providers
- **THEN** an INFO log is written with provider_id, name, and "created" action

#### Scenario: Provider updated
- **WHEN** a provider is successfully updated via PUT /api/providers/:id
- **THEN** an INFO log is written with provider_id and "updated" action

#### Scenario: Provider deleted
- **WHEN** a provider is soft-deleted via DELETE /api/providers/:id
- **THEN** an INFO log is written with provider_id and "deleted" action

#### Scenario: Provider not found
- **WHEN** a provider lookup by id returns no result
- **THEN** a WARNING log is written with the requested provider_id

### Requirement: API test requests are logged
The system SHALL log test-api requests with provider base_url and api_path.

#### Scenario: Test API request
- **WHEN** POST /api/providers/test-api is called
- **THEN** an INFO log records the base_url and api_path being tested (API key is NOT logged)

### Requirement: Manual collection triggers are logged
The system SHALL log manual collection triggers and their outcomes.

#### Scenario: Manual collection triggered
- **WHEN** POST /api/providers/:id/collect is called
- **THEN** an INFO log records the provider_id and collection trigger

#### Scenario: Collection succeeded
- **WHEN** usage or balance collection completes without errors
- **THEN** an INFO log records provider_id, record_count (for usage), and balance value (for balance)

#### Scenario: Collection failed
- **WHEN** collection encounters an exception
- **THEN** an ERROR log records provider_id and the exception message

### Requirement: Stats queries are logged
The system SHALL log summary, trends, and distribution queries with relevant filter parameters.

#### Scenario: Summary query
- **WHEN** GET /api/stats/summary is called
- **THEN** an INFO log records the provider_id filter if specified

### Requirement: Scheduler job lifecycle is logged
The system SHALL log job registration, removal, and rescheduling events.

#### Scenario: Job registered
- **WHEN** a scheduled collection job is registered for a provider
- **THEN** an INFO log records provider_id and interval_seconds

#### Scenario: Job removed
- **WHEN** a scheduled collection job is removed
- **THEN** an INFO log records provider_id

#### Scenario: Job rescheduled
- **WHEN** a provider's interval is changed causing job rescheduling
- **THEN** an INFO log records provider_id and new_interval
