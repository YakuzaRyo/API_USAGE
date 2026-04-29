## ADDED Requirements

### Requirement: Configurable JSONPath response mapping

The system SHALL allow users to configure dot-notation JSON paths to extract usage fields (total_tokens, cost) and balance fields (balance) from LLM provider API responses. Parsing SHALL be driven entirely by user-configured mapping with no hardcoded format detectors.

#### Scenario: User configures mapping for DeepSeek balance format

- **WHEN** user configures `balance_mapping: {"balance": "balance_infos.0.total_balance"}` and balance API returns `{"balance_infos": [{"total_balance": "5.60"}]}`
- **THEN** the collector extracts `balance = 5.60` and stores it

#### Scenario: Mapping path does not exist in response

- **WHEN** a mapping path points to a non-existent key
- **THEN** the collector returns 0 or None for that field and logs a warning

### Requirement: Test API endpoint returns raw JSON

The system SHALL provide a `POST /api/providers/test-api` endpoint that accepts temporary base_url, api_key, and api_path, makes the HTTP request, and returns the raw JSON response body regardless of status code.

#### Scenario: Test API with valid path

- **WHEN** user submits test with valid URL and API key
- **THEN** the raw JSON response body is returned for inspection

#### Scenario: Test API with error

- **WHEN** user submits test and the external API returns 401
- **THEN** the response body from the external API is returned alongside the HTTP status code

### Requirement: Currency symbol configuration

The system SHALL store a `currency_symbol` per provider (default "CNY") and SHALL use it in Dashboard balance display.

#### Scenario: Dashboard shows balance with configured symbol

- **WHEN** a provider has `currency_symbol: "¥"` and `last_balance: 5.60`
- **THEN** the Dashboard balance card displays "5.60 ¥"
