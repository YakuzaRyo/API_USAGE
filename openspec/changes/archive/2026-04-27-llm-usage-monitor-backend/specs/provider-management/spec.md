## ADDED Requirements

### Requirement: List all providers

The system SHALL return a list of all configured providers with api_key masked to show only the last 4 characters. The response SHALL include id, name, masked api_key, base_url, usage_api_path, models list, interval_seconds, and created_at.

#### Scenario: List providers

- **WHEN** `GET /api/providers` is called
- **THEN** the response contains an array of provider objects with masked api_key (e.g., `sk-...xxxx`)

### Requirement: Create a provider

The system SHALL accept provider creation with name, api_key, base_url, usage_api_path (default `/v1/usage`), models (JSON array), and interval_seconds (0 for manual, >= 10 for auto). api_key SHALL be encrypted via Fernet before storage.

#### Scenario: Successful creation

- **WHEN** `POST /api/providers` with valid fields is called
- **THEN** the provider is stored with encrypted api_key and returned with status 200

#### Scenario: Validation failure

- **WHEN** `POST /api/providers` with empty name or api_key or base_url
- **THEN** returns 422 with validation error detail

### Requirement: Update a provider

The system SHALL allow updating any provider field via `PUT /api/providers/{id}`. If a new api_key is provided, it SHALL be re-encrypted.

#### Scenario: Successful update

- **WHEN** `PUT /api/providers/{id}` with changed fields is called
- **THEN** the provider is updated and the updated object returned

#### Scenario: Update non-existent provider

- **WHEN** `PUT /api/providers/999` is called for a non-existent ID
- **THEN** returns 404

### Requirement: Delete a provider

The system SHALL soft-delete a provider via `DELETE /api/providers/{id}`. Usage records belonging to the deleted provider SHALL be retained.

#### Scenario: Successful delete

- **WHEN** `DELETE /api/providers/{id}` is called
- **THEN** the provider is marked deleted and usage records remain queryable

#### Scenario: Delete non-existent provider

- **WHEN** `DELETE /api/providers/999` is called
- **THEN** returns 404

### Requirement: Test provider connection

The system SHALL test connectivity by making an HTTP GET request to `{base_url}{usage_api_path}` with `Authorization: Bearer {api_key}`. The response SHALL indicate success or failure with error details.

#### Scenario: Connection succeeds

- **WHEN** `POST /api/providers/{id}/test` is called and the external API returns 2xx
- **THEN** returns `{"status": "ok"}`

#### Scenario: Connection fails

- **WHEN** `POST /api/providers/{id}/test` is called and the external API returns 4xx/5xx or network error
- **THEN** returns `{"status": "error", "message": "<reason>"}`
